# https://stackoverflow.com/questions/43006368/connecting-with-athena-using-python-and-pyathenajdbc?rq=1
#https://qingstudios.com/2020/04/01/query_aws/

from pyathena import connect
import sys,re
import pandas as pd

conn = connect(role_arn="arn:aws:iam::129:role/mydatabase.dev",
               region_name="us-west-2", work_group="myworkgroup",aws_access_key_id='AXYDA',aws_secret_access_key='theKey')
'''
conn = connect(region_name="us-west-2"
               ,aws_access_key_id='rrrrr'
               ,aws_secret_access_key='aaaaa'
               ,aws_session_token='yyyyy'
               ,s3_staging_dir="s3://aws-athena-query-results-5566565656-us-west-2/users/userid/"
               ,work_group="users")
'''
cur = conn.cursor()

sql_query = "SHOW DATABASES"
sql_query = "SHOW TABLES IN  mydatabase"

sql_query = 'SHOW COLUMNS FROM myschema.mytable'
dataEx = cur.execute(sql_query)

data = dataEx.fetchall()

tabStruct = []

for row in data:
    rowSplit = row[0].split('\t')
    if not rowSplit[1].startswith('row'):
        tabStruct.append(['base'] + rowSplit)
        print(rowSplit)


for row in data:
    rowSplit = row[0].split('\t')
    if rowSplit[1].startswith('row'):
        da = rowSplit[1]
        da = da.replace('row(','')
        da = re.sub('\(|\)|\"','',da)

        for colrow in da.split(','):
            tabStruct.append(['json'] + colrow.split(' '))
            print(colrow.split(' '))

print(tabStruct)
