import os
import pandas as pd

file = 'dashboard-label'
base = "./data/"
config = os.path.join(base,file +'.tsv')

sourceall = pd.read_csv(config, header=0, sep="\t")
# sourcefilter = sourceall.copy()

listOfDashboards = list(sourceall['workbook'].unique())

alldata = pd.DataFrame()

for workbook in listOfDashboards:
    sourcefilter = sourceall[sourceall['workbook'] == workbook][['label']].drop_duplicates()
    sourceOther = sourceall[sourceall['workbook'] != workbook][['label','workbook']]
    sourceMerged = sourcefilter.merge(sourceOther, on=['label'],how='inner')
    sourceMerged['masterworkbook'] = workbook
    sourceMerged['attrcount'] = sourcefilter.shape[0]
    alldata = alldata.append(sourceMerged)

alldata = alldata.drop_duplicates()
alldata.to_csv( os.path.join(base,file +'_detail.tsv'), header=True,index=False,sep='\t')
alldata.groupby(['masterworkbook','attrcount','workbook']).count().reset_index().to_csv( os.path.join(base,file +'_summary.tsv'), header=True,index=False,sep='\t')
