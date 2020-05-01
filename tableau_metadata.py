from tableaudocumentapi import Workbook, Datasource
import os
import pandas as pd

baseLoc = "../../data/"
baseTab = os.path.join(baseLoc, 'tableau')
baseTabout = os.path.join(baseLoc, 'tableauout')
Details = []
for file in os.listdir(baseTab):

    sourceWB = Workbook(os.path.join(baseTab,file))
    worksheets = sourceWB.worksheets

    for worksheet in worksheets:

        for datasource in sourceWB.datasources:
            for count, field in enumerate(datasource.fields.values()):

                for fieldWorksheet in field.worksheets:

                    if worksheet == fieldWorksheet:
                        # print(file,worksheet, "==", fieldWorksheet, "|", count, field.name, "-", field.caption)
                        Details.append([file,worksheet, count, field.name, field.caption])

df = pd.DataFrame.from_records(Details,columns=['workbook','worksheet','fieldnumber','name','label'])
df.to_csv(os.path.join(baseTabout, 'wbfields.tsv'),header=True,index=False,sep='\t')
