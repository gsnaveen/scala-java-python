from simple_salesforce import SalesforceLogin,Salesforce, SFType
from pprint import pprint as pp
import pandas as pd
import os

sfdc_username='me@my.com'
sfdc_password='mypassword'
sfdc_security_token='tokenXYZ'

session_id , instance = SalesforceLogin(username=sfdc_username,
                                  password=sfdc_password,
                                  security_token=sfdc_security_token)


sf = Salesforce(instance=instance,session_id=session_id)

targetFolder = './data/sfdc/'
baseDataAtttr = ['reportid','reportName','Typelabel','Type']
allreportColList = []
allreportFilterList = []
allreportDateFilterList = []

report_id_list = ['xx','yy','zz']

for report_id in report_id_list:

    report_results = sf.restful('analytics/reports/{}'.format(report_id))

    reportName = report_results['attributes']['reportName']
    reportreportTypeLabel = report_results['reportMetadata']['reportType']['label']
    reportreportTypeType = report_results['reportMetadata']['reportType']['type']

    baseData = [report_id,reportName,reportreportTypeLabel,reportreportTypeType]
    reportColList = []
    reportFilterList = []
    reportDateFilterList = []

    #List
    reportColumns = report_results['reportMetadata']['detailColumns']
    for col in reportColumns:
        reportColList.append(baseData + [col])

    #List
    reportreportFilters = report_results['reportMetadata']['reportFilters']
    for fltr in reportreportFilters:
        reportFilterList.append(baseData + [fltr['column'],fltr['operator'],fltr['value']])


    #Date input filter
    reportstandardDateFilter = report_results['reportMetadata']['standardDateFilter']
    reportDateFilterList.append(baseData + [reportstandardDateFilter['column'],reportstandardDateFilter['durationValue']])

    allreportColList.extend(reportColList)
    allreportFilterList.extend(reportFilterList)
    allreportDateFilterList.extend(reportDateFilterList)

df = pd.DataFrame.from_records(allreportColList,columns=[ baseDataAtttr + ['attribute']])
df.to_csv(os.path.join(targetFolder,'Salesforce_reportAttributes_out.tsv'),header=True, sep='\t', index=False)

df = pd.DataFrame.from_records(allreportFilterList,columns=[ baseDataAtttr + ['attribute','operator','value']])
df.to_csv(os.path.join(targetFolder,'Salesforce_reportFilters_out.tsv'),header=True, sep='\t', index=False)

df = pd.DataFrame.from_records(allreportDateFilterList,columns=[ baseDataAtttr + ['attribute','duration']])
df.to_csv(os.path.join(targetFolder,'Salesforce_reportDateFilter_out.tsv'),header=True, sep='\t', index=False)




"""
for key in report_results:
    print(key)

    if key == 'reportMetadata':
        print(key, report_results[key]['detailColumns'], report_results[key])
        pp(report_results[key])
        
--Keys in the returned dataset
attributes
allData
factMap
groupingsAcross
groupingsDown
hasDetailRows
picklistColors
reportExtendedMetadata
reportMetadata


https://developer.salesforce.com/docs/atlas.en-us.api_analytics.meta/api_analytics/sforce_analytics_rest_api_report_query.htm
"""
