
import pandas as pd
import sqlite3
import duckdb

#pip install xlsxwriter
writer = pd.ExcelWriter('datacatalog_excel.xlsx', engine='xlsxwriter')
connSQLlite = sqlite3.connect("datacatalog_sqlite.db")
duckdbconn = duckdb.connect("datacatalog_duckdb.db")

data = [('A','AA'),('A','AAA'), ('B','BB'), ('B','BBB')]
df = pd.DataFrame.from_records(data, columns=['entity','attribute'])

df.to_excel(writer,sheet_name="Table-Entity",startrow=0, startcol=0,index=False)
df.to_sql('tablex', connSQLlite, if_exists='replace', index = False)
duckdbconn.sql("CREATE TABLE {target_table} AS SELECT * FROM {sourcedf}".format(target_table= 'meta_entity', sourcedf='df'))
# duckdbconn.sql("CREATE TABLE {database}.main.{target_table} AS SELECT * FROM {sourcedf}".format(database='datacatalog',target_table= 'summarysheet', sourcedf='dfsummarySheet'))
writer._save()
duckdbconn.close()
