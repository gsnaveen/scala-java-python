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

""" """    
textDtype = ['string']
numDtype = ['int','bigint']
SQL = 'Select count(*) Records,'
df = pd.read_csv("./data/dataCheckTable.txt",sep='\t',header='infer')
"""
column	datatype
eventtype	string
eventdatetime	bigint
visitid	string
eventid	string
hour_of_the_view	int
keyword	string
auto_suggest	string
"""
for index,row in df.iterrows():
    if row['datatype'].lower() in textDtype:
        col = "sum(case when " + row['column'] + " != '-'" + " and " + row['column'] + " != ''" + " then 1 End ) " + row['column']
        coldmm = "count(distinct " + row['column'] + ") " + row['column'] + "_unique_values" + ", max(length( " + row['column'] + ")) " + row['column'] + "_max_len"
        #print(row['column'])
    elif row['datatype'].lower() in numDtype:
        col = "sum(case when " + row['column'] + " > 0 then 1 End ) " + row['column']
        coldmm = "min(" + row['column'] + ") " + row['column'] + "_min" + ", max(" + row['column'] + ") " + row['column'] + "_max"
        #print(row['column'])
    SQL += col + ',\n' + coldmm + ',\n'
print(SQL)        
