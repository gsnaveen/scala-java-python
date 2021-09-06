import os
import pandas as pd
from sqlalchemy import create_engine

DATA = './data/'
alchemyEngine = create_engine('postgresql+psycopg2://{userid}:{pword}@{host}/{db}'.format(userid=userid, pword=passWord,
                                                                                      db=database,port=port,host=host), pool_recycle=3600);
postgreSQLConnection = alchemyEngine.connect();

file = 'csv'
conn = postgreSQLConnection
tableSchemaSQLbase = '''select column_name,data_type from information_schema.columns
                    where table_name = '{table_name}'
                    and table_schema='{table_schema}'
                    '''
schemaName = 'metadata'
folder = 'metadata_file'
fileName = 'loadData'
tableName = 'metadata_file'.format(schema=schemaName)

tableSchemaSQL = tableSchemaSQLbase.format(table_schema=schemaName, table_name=tableName)

tabelDeffdata = conn.execute(tableSchemaSQL)
tabelDeffList = tabelDeffdata.fetchall()

tabDeff = {}
for row in tabelDeffList:
    tabDeff[row[0]] = row[1]

infile = os.path.join(DATA, 'toDB', folder, fileName + '.tsv')

df = pd.read_csv(infile, header=0, sep='\t')
dataCols = set(df.columns)
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
    for col in tabDiffInData:

        if tabDeff[col] in ['integer', 'bigint', 'double precision', 'numeric']:
            valuesStr += "{val},".format(val=row[col])
        else:
            valuesStr += "'{val}',".format(val=row[col])

    else:
        if numRows == index + 1:
            valuesStr += 'current_timestamp); \n'
        else:
            valuesStr += 'current_timestamp), \n'

insertStmt = insertSQLHeader + valuesStr

try:
    conn.execute(insertStmt)
except:
    raise
    print("Insert error")
