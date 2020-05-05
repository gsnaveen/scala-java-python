from tableaudocumentapi import Workbook, Datasource
import os
import pandas as pd

baseLoc = "../../data/"
baseTab = os.path.join(baseLoc, 'tableau')
baseTabout = os.path.join(baseLoc, 'tableauout')
Details = []
print(baseTab)
for file in os.listdir(baseTab):
    if file.endswith(".twbx"):
        # print(file)
        sourceWB = Workbook(os.path.join(baseTab,file))
        worksheets = sourceWB.worksheets

        for worksheet in worksheets:

            for datasource in sourceWB.datasources:
                for count, field in enumerate(datasource.fields.values()):

                    for fieldWorksheet in field.worksheets:

                        if worksheet == fieldWorksheet:
                            # print(file,worksheet, "==", fieldWorksheet, "|", count, field.name, "-", field.caption)
                            Details.append([file,worksheet,datasource.caption, count, field.name, field.caption,field.role])

detailsdc = []
for file in os.listdir(baseTab):
    if file.endswith(".twbx"):
        # print(file)
        sourceWB = Workbook(os.path.join(baseTab, file))

        for ds in sourceWB.datasources:
            for field,value in ds.fields.items():
                # print(ds.caption,field,value.name,value.caption,value.alias,value.role,value.datatype)
                detailsdc.append([file,ds.caption,field,value.name,value.caption,value.alias,value.role])

df = pd.DataFrame.from_records(Details,columns=['workbook','worksheet','connection','fieldnumber','name','label','type'])
df.to_csv(os.path.join(baseTabout, 'wbfields.tsv'),header=True,index=False,sep='\t')
df = pd.DataFrame.from_records(detailsdc,columns=['workbook','connection','fieldname','name','caption','alias','role'])
df.to_csv(os.path.join(baseTabout, 'wbfieldscon.tsv'),header=True,index=False,sep='\t')
