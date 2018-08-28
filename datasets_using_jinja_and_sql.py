#https://overiq.com/flask/0.12/basics-of-jinja-template-language/
#https://stackoverflow.com/questions/8260490/how-to-get-list-of-all-variables-in-jinja-2-templates
#http://jinja.pocoo.org/docs/2.10/templates/
from jinja2 import Template,FileSystemLoader,Environment
import pyodbc
import pandas as pd
import re,sys,os

DataSet = "" #"SUMMARY" #SUMMARY/DETAIL
datafor = "product1"
RunID = "jan-2018"
DataSetFolder = ""
dataSetName = datafor +"_"+RunID

startdate = '2018-06-01'
enddate = '2018-06-01'
url = '//www.mydomain.com/'
context = {'StartDate': startdate, 'EndDate': enddate, 'url': url} #, 'url2':'//www.iamurl2.com/'
jinja_env = Environment(loader=FileSystemLoader('./template/'),trim_blocks=True, lstrip_blocks=True)
template = jinja_env.get_template('main.sql.j2')

cursor = pyodbc.connect("DSN=hiveProd2",autocommit=True)
cursor.execute('SET mapreduce.reduce.memory.mb=8192')
cursor.execute('SET mapreduce.reduce.java.opts=-Xmx6144m')
cursor.execute('SET mapreduce.map.memory.mb=8192')
cursor.execute('SET mapreduce.map.java.opts=-Xmx6144m')
cursor.execute('SET hive.execution.engine=mr')
cursor.setencoding('utf-8')


def getdata(dset,SQL,hivecon=cursor):
    databasedf = pd.read_sql_query(SQL, hivecon)
    databasedf.to_csv("./data/"+dset+".csv",sep='\t',header=True, index=False)
    with open("./data/"+dset+".sql",'w') as f:
        f.write(SQL)
        

sqlname= None; mainSQL = "";SqlStart= False
SQLDict = {}   

for SQLline in template.render(context).splitlines():
    
    if SQLline == "" or SQLline.find("###") == 0: 
        continue
    elif SQLline.find("SQLNAME") == 0: 
        SqlStart = True;  sqlname = SQLline.split("=")[1] ; mainSQL = ""
    elif SQLline=="SQLEND":
        SQLDict[sqlname] = re.sub(' +',' ',mainSQL).strip()
        SqlStart = False; sqlname = None; mainSQL = ""
    elif SqlStart == True and sqlname != None and SQLline !="SQLEND":
        if SQLline.find("###") > 0:
            mainSQL += " " + SQLline.split("###")[0]
        else:
            mainSQL += " " + SQLline
        
for report,SQL in SQLDict.items():
    report = dataSetName+"_"+report
    if DataSet != "" and report.endswith(DataSet):
        getdata(report,SQL)
    else:
        getdata(report,SQL)
        
""" 
### main.sql.j2

{% include "page.sql.j2" %}

{% include "./events/events.sql.j2" %}

{% include "cpr.sql.j2" %}
"""
