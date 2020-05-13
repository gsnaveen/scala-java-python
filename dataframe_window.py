import pandas as pd
import os

"""
dated	dow	rows
2020-04-12	0	1600
2020-04-13	1	2911
2020-04-14	2	4199
2020-04-15	3	3500
2020-04-16	4	6422
2020-04-17	5	5001
2020-04-18	6	2000
"""

# Config
dataFolder = './data/'
file = 'dataLoads'
dateCol = 'response_date'
dowCol = 'dow'
metricCol = 'response'

df = pd.read_csv(os.path.join(dataFolder,file +".tsv"),header=0,sep='\t')
df = df.sort_values(dateCol)
# df['response_date'] = pd.to_datetime(df['response_date'].str.strip(),format='%Y-%m-%d')
df[dateCol] = pd.to_datetime(df[dateCol],yearfirst=True)
df['4WRolling'] = df[metricCol].rolling(28).mean().round()
df['4WRollingStd'] = df[metricCol].rolling(28).std().round()
df['7Rolling'] = df[metricCol].rolling(7).mean().round()
df['7RollingStd'] = df[metricCol].rolling(7).std().round()

forvalueLoopData_rolling_all = pd.DataFrame()
forLoop = df[dowCol].unique()
for i in forLoop:
    forvalueLoopData = df[df[dowCol] == i][[dateCol,metricCol]].sort_values(dateCol)
    forvalueLoopData['dowAvg'] = forvalueLoopData[metricCol].rolling(4).mean().round()
    forvalueLoopData['dowStd'] = forvalueLoopData[metricCol].rolling(4).std().round()
    forvalueLoopData_rolling_all = forvalueLoopData_rolling_all.append(forvalueLoopData)

df = df.merge(forvalueLoopData_rolling_all,on=[dateCol,metricCol],how='inner')

df.to_csv(os.path.join(dataFolder,file +"_out.tsv"),header=True,sep='\t',index=False)
print(df.dtypes)
print(df.tail(100))
