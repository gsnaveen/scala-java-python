import os
import psycopg2
import pandas as pd

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
    
from modules.configs import *
from modules.postgres import *

tableAccess = """SELECT table_schema ||'.'|| table_name entity, grantee
FROM   information_schema.table_privileges 
WHERE  grantee is not null 
and privilege_type in ('SELECT') 
and grantee in ({users})
and table_schema ||'.'|| table_name in ({tables})"""

grantAccess = """GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE {tab} TO {usr};"""

opertype = "grant" # "granted" "grant"
preFix = "grant"

entityList = pd.read_csv(DATA+ preFix + "_entityList.txt",header=0,sep='\t')
usersList = pd.read_csv(DATA + preFix + "_users.txt",header=0,sep='\t')


users = []
entity = []

for index, row in usersList.iterrows():
    users.append(row['user'].split('@')[0])

for index, row in entityList.iterrows():
    entity.append(row['entity'])

userSQl = str(users).replace('[','').replace(']','')
entitySQL = str(entity).replace('[','').replace(']','')

if opertype == "granted":

    theSelect = tableAccess.format(users=userSQl, tables =entitySQL)
    print(theSelect)

    try:
        theResult = pd.read_sql_query(theSelect, con=conn)
        pass
    except:
            print("Error")

    entityList['grantee'] = 'admin'

    theResult = theResult.append(entityList)
    theResult.to_csv(os.path.join(DATA + "accessList.tsv"), sep='\t', header=True, index=False)

elif opertype == "grant":
    granted = []
    for user in users:
        for tab in entity:
            sql = grantAccess.format(tab=tab,usr=user)
            try:
                theResult = cur.execute(sql)
                granted.append([user,tab,'granted'])
            except Exception as e:
                print("SQL error for {usr} on table {tab} with error {err}".format(tab=tab,usr=user,err=e))
                granted.append([user, tab, 'error'])
    conn.commit()
    cur.close()
    conn.close()
