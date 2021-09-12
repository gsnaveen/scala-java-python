import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

DATA = './data/'
"""
alchemyEngine = create_engine('postgresql+psycopg2://{userid}:{pword}@{host}/{db}'.format(userid=userid, pword=passWord,
                                                                                      db=database,port=port,host=host), pool_recycle=3600);
postgreSQLConnection = alchemyEngine.connect();
"""

try:
    conn = psycopg2.connect(
        "dbname={db} user={userid} host={host} port={port} password={pword}".format(userid=userid, pword=passWord,
                                                                                    db=database, port=port,
                                                                                    host=host))
except Exception as ex:
    print("I am unable to connect to the database" + str(ex))

cur = conn.cursor()
    

file = 'csv'
conn = postgreSQLConnection
tableSchemaSQLbase = '''select column_name,data_type from information_schema.columns
                    where table_name = '{table_name}'
                    and table_schema='{table_schema}'
                    '''
schemaName = 'metadata'
folder = 'metadata_file'
fileName = 'loadData'
tableName = 'metadata_file'

tableSchemaSQL = tableSchemaSQLbase.format(table_schema=schemaName, table_name=tableName)

cur.execute(tableSchemaSQL)
tabelDeffList = cur.fetchall()

tabDeff = {}
for row in tabelDeffList:
    tabDeff[row[0]] = row[1]

infile = os.path.join(DATA, 'ps', 'toDB', folder, fileName + '.tsv')

df = pd.read_csv(infile, header=0, sep='\t')
df.columns = [col.lower() for col in df.columns ]
dataCols = set(df.columns)
print(dataCols)
numRows = df.shape[0]

dataColsInDB = [col for col in dataCols if col in tabDeff]
dataColsInDBNot = [col for col in dataCols if col not in tabDeff]

tabDiffInData = [col for col in tabDeff if col in dataCols]
tabDiffInDataNot = [col for col in tabDeff if col not in dataCols and col != 'load_datetime']

print('Not In table {schema}.{tab}'.format(schema=schemaName, tab=tableName), dataColsInDBNot)
print('Not In InputFile {tab}'.format(tab=fileName), tabDiffInDataNot)
print('Number of rows {numrows}'.format(numrows=numRows))

toInsertAttr = ','.join((tabDiffInData + ['load_datetime']))

insertSQLHeader = '''
                    INSERT INTO 
                        {schema}.{table} ({toInsertAttr})
                    VALUES
                    '''.format(schema=schemaName, table=tableName, toInsertAttr=toInsertAttr)
valuesStr = ''

for index, row in df.iterrows():
    valuesStr += '('
    valuesStr1 = '('
    for col in tabDiffInData:

        theVal = "{val}".format(val=row[col]).strip()
        theVal = re.sub("'","''",theVal)
        if (theVal == 'nan') or (pd.isna(theVal)) or (pd.isnull(theVal)) or (theVal == None) or (theVal == ''):
            theVal = 'null'

        if tabDeff[col] in ['integer', 'bigint', 'double precision', 'numeric']:
            valuesStr += "{val},".format(val=theVal)
            valuesStr1 += "{val},".format(val=theVal)

        elif theVal == 'null':
            valuesStr += "{val},".format(val=theVal)
            valuesStr1 += "{val},".format(val=theVal)
        else:
            valuesStr += "'{val}',".format(val=theVal)
            valuesStr1 += "'{val}',".format(val=theVal)

    else:
        valuesStr1 += 'current_timestamp);'
        if numRows == index + 1:
            valuesStr += 'current_timestamp); \n'
        else:
            valuesStr += 'current_timestamp), \n'

    if insert1 :
        try:
            cur.execute(insertSQLHeader + valuesStr1)
            conn.commit()
        except:
            insertErrors.append(index)
            print(index,insertSQLHeader + valuesStr1)


if not insert1 :
    try:
        insertStmt = insertSQLHeader + valuesStr
        print(insertStmt)
        cur.execute(insertStmt)
        conn.commit()
    except:
        print("Insert error")
        raise

cur.close()
conn.close()
