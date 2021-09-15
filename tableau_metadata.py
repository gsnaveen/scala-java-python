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

'''
with base0 as (select distinct workbook, attrname, lower(caption) caption, attrtype, lower(keyword) keyword
						from optics.tableau_sheetfields where keyword is not null
						),
base1count as (select workbook, attrname, caption, attrtype, count(*) words
				from base0 group by workbook, attrname, caption, attrtype),
base as ( select base0.workbook, base0.attrname, base0.caption, base0.attrtype,base1count.words,base0.keyword
		from base0 inner join base1count on
		base0.workbook = base1count.workbook and base0.attrname = base1count.attrname
		and  base0.caption = base1count.caption and  base0.attrtype = base1count.attrtype),
keySecond as (select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words,da1.keyword keyword1, case when da1.words > 1 then da2.keyword else null end keyword2
				from base da1 inner join base da2 on
				da1.workbook = da2.workbook and da1.attrname = da2.attrname
				and  da1.caption = da2.caption and da1.attrtype = da2.attrtype),
key3rd as (select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1, da1.keyword2, case when da1.words > 2 then da2.keyword else null end keyword3
				from keySecond da1 inner join base da2 on
				da1.workbook = da2.workbook and da1.attrname = da2.attrname
				and  da1.caption = da2.caption and da1.attrtype = da2.attrtype),
key4th as (select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1, da1.keyword2,da1.keyword3 ,case when da1.words > 3 then da2.keyword else null end keyword4
				from key3rd da1 inner join base da2 on
				da1.workbook = da2.workbook and da1.attrname = da2.attrname
				and  da1.caption = da2.caption and da1.attrtype = da2.attrtype),
baseUnion as (select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4,count(*) times
			from key4th da1 where words =1
			group by da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4
		 union all
		 select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4,count(*) times
			from key4th da1 where words =2 and keyword1 != keyword2
			group by da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4
		union all
		 select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4,count(*) times
			from key4th da1 where words =3 and ((keyword1 != keyword2 and keyword1 != keyword3) and (keyword2 != keyword3))
			group by da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4
		union all
		 select distinct da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4,count(*) times
			from key4th da1 where words > 3 and ((keyword1 != keyword2 and keyword1 != keyword3 and keyword1 != keyword4) and (keyword2 != keyword3 and keyword2 != keyword4) and ((keyword3 != keyword4)))
			group by da1.workbook, da1.attrname, da1.caption, da1.attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4
--			where keyword1 != coalesce(keyword2,'') and keyword1 != coalesce(keyword3,'') and keyword1 != coalesce(keyword4,'')
--					and coalesce(keyword2,' ') != coalesce(keyword3,'') and coalesce(keyword2,' ') != coalesce(keyword4,'') and coalesce(keyword3,'  ') != coalesce(keyword4,'')
			)
select workbook,da1.caption,attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4,Sum(times) times
from baseUnion da1
group by workbook,da1.caption,attrtype, da1.words, da1.keyword1 , da1.keyword2 , da1.keyword3,da1.keyword4
'''
