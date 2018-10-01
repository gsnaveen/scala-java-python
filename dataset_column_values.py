import pyodbc
import pandas as pd
cursor = pyodbc.connect("DSN=hiveProd2",autocommit=True)
# cursor = hivecon.cursor()
cursor.execute('SET mapreduce.reduce.memory.mb=8192')
cursor.execute('SET mapreduce.reduce.java.opts=-Xmx6144m')
cursor.execute('SET mapreduce.map.memory.mb=8192')
cursor.execute('SET mapreduce.map.java.opts=-Xmx6144m')
cursor.execute('SET hive.execution.engine=mr')
# cursor.setencoding('utf-8')

source = pd.read_csv("./data/columnvalues.tsv",header=0,sep="\t")

"""
tablename	column	complextype
tablename1	title	params
tablename1	breakpoint	params
"""
    
TABLENAME = 'tablename'
COLUMNNAME = 'column'
COMPLEXTYPE = 'complextype'

for index,row in source.iterrows():
    
    SQL_SELECT = "Select distinct "
    SQL_FROM = " from " + row[TABLENAME]
    SQL_WHERE = " where viewdate = '2018-09-25' limit 100"
    
    if row[COMPLEXTYPE] == "":
        SQL_COLUMN =  row[COLUMNNAME]
        fileName = row[TABLENAME] +"."+ row[COLUMNNAME]
    else:
        SQL_COLUMN =  row[COMPLEXTYPE] + '["' + row[COLUMNNAME] +'"]' + " " + row[COLUMNNAME].replace(".","_")
        fileName = row[TABLENAME] + "."+ row[COMPLEXTYPE] + "."+ row[COLUMNNAME]
        
    theSelect = SQL_SELECT + SQL_COLUMN + SQL_FROM + SQL_WHERE
    
    Hivedf = pd.read_sql_query(theSelect , cursor)
    Hivedf.to_csv("./data/" + fileName + "_data.tsv",sep='\t',header=True, index=False)
