from tableaudocumentapi import Workbook, Datasource
import os
import pandas as pd

baseLoc = "../../data/"
baseTab = os.path.join(baseLoc, 'tableau')
baseTabout = os.path.join(baseLoc, 'tableauout')

Details = []
DetailsKeyword = []
extension = 'twbx' # 'twbx' 'twb'

def cleanText (inStr):

    base1 = re.sub('\[|\]|\(|\)|\"', '', inStr)
    base2 = re.sub('_', ' ', base1)
    base3 = re.sub('\s+', ' ', base2)

    lastStr = base3.lower()

    return lastStr.split(' ')

print(baseTab)


for file in os.listdir(baseTab):
    if file.endswith("."+extension):
        sourceWB = Workbook(os.path.join(baseTab,file))
        worksheets = sourceWB.worksheets

        for worksheet in worksheets:

            for datasource in sourceWB.datasources:
                for count, field in enumerate(datasource.fields.values()):

                    for fieldWorksheet in field.worksheets:

                        if worksheet == fieldWorksheet:
                            typeCol = calcSource = ''
                            if re.search('\(group\)', field.id) : typeCol = 'grouping'
                            if re.search('Calculation\_', field.id):
                                typeCol = 'Calculation'
                                calcSource = field.calculation

                            fieldID = re.sub('\[|\]','',field.id)

                            Details.append([file,worksheet,datasource.caption, count, fieldID, field.name,field.role,typeCol,calcSource,None]) # field.caption

                            for keyword in cleanText(field.name):
                                DetailsKeyword.append(
                                    [file, worksheet, datasource.caption, count, fieldID, field.name, field.role,
                                     typeCol, calcSource, None,keyword])

detailsdc = []
detailsdcKeyword = []
for file in os.listdir(baseTab):
    if file.endswith("."+extension):
        sourceWB = Workbook(os.path.join(baseTab, file))

        for ds in sourceWB.datasources:
            for field,value in ds.fields.items():
                detailsdc.append([file,ds.caption,re.sub('\[|\]','',field),value.name,value.caption,value.alias,value.role])
                for keyword in cleanText(value.name):
                    detailsdcKeyword.append(
                        [file, ds.caption, re.sub('\[|\]', '', field), value.name, value.caption, value.alias,
                         value.role,keyword])

df = pd.DataFrame.from_records(Details,columns=['workbook','worksheet','connection','fieldnumber','name','label','type','grpCalc','calcSource','basetable'])
df.to_csv(os.path.join(baseTabout, extension + '_wbfields.tsv'),header=True,index=False,sep='\t')
df = pd.DataFrame.from_records(DetailsKeyword,columns=['workbook','worksheet','connection','fieldnumber','name','label','type','grpCalc','calcSource','basetable','keyword'])
df.to_csv(os.path.join(baseTabout, extension + '_wbfields_keyword.tsv'),header=True,index=False,sep='\t')

df = pd.DataFrame.from_records(detailsdc,columns=['workbook','connection','fieldname','name','caption','alias','role'])
df.to_csv(os.path.join(baseTabout, extension + '_wbfieldscon.tsv'),header=True,index=False,sep='\t')
df = pd.DataFrame.from_records(detailsdcKeyword,columns=['workbook','connection','fieldname','name','caption','alias','role','keyword'])
df.to_csv(os.path.join(baseTabout, extension + '_wbfieldscon_keyword.tsv'),header=True,index=False,sep='\t')
