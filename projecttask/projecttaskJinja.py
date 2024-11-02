import jinja2 as jin
import pandas as pd
import json
inputFolder = './input/'; outputFolder = './output/'
inputFile = 'reports'; outputFile = inputFile+'_tasklist'

jinja_env = jin.Environment(loader=jin.FileSystemLoader('./template/'),trim_blocks=True, lstrip_blocks=True)
template = jinja_env.get_template('reports.j2')
inputdf = pd.read_csv(inputFolder+inputFile +'.tsv',header=0,sep='\t')

summaryList = []; detailtaskList = []

for index, rowy in inputdf.iterrows():
    dataProduct = rowy['DataProduct']; timeLine = rowy['Timeline']
    for reportName, complexity in eval(rowy['Reports']).items():
        context = {'reports': [reportName], 'DataProduct': dataProduct, 'Timeline': timeLine}
        for row in template.render(context).splitlines():
            rowSplit = row.split('|')
            patentOrChild = 'Parent' if rowSplit[2] == rowSplit[3] else 'Child'

            if patentOrChild == 'Parent':
                summaryList.append([rowSplit[0],rowSplit[1],reportName,rowSplit[2],complexity])

            detailtaskList.append([rowSplit[0],rowSplit[1],reportName,rowSplit[2],rowSplit[3],patentOrChild,complexity])


dfSummary = pd.DataFrame.from_records(summaryList,columns=['DataProduct','TimeLine','ReportName','Stage','Complexity'])
dfDetailtask = pd.DataFrame.from_records(detailtaskList,columns=['DataProduct','TimeLine','ReportName','Stage','Task','parentOrChild','Complexity'])
writer = pd.ExcelWriter(outputFolder+outputFile+'.xlsx', engine='xlsxwriter')
dfSummary.to_excel(writer,sheet_name="Summary",startrow=0, startcol=0,index=False)
dfDetailtask.to_excel(writer,sheet_name="Detail-Task",startrow=0, startcol=0,index=False)
writer._save()
# print(summaryList)
# print(detailtaskList)