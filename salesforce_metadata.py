from simple_salesforce import SalesforceLogin,Salesforce, SFType
from pprint import pprint as pp
import pandas as pd
import os

sfdc_username='me@my.com'
sfdc_password='mypassword'
sfdc_security_token='tokenXYZ'

targetFolder = './data/sfdc/'

session_id , instance = SalesforceLogin(username=sfdc_username,
                                  password=sfdc_password,
                                  security_token=sfdc_security_token)

sf = Salesforce(instance=instance,session_id=session_id)


dfObjects = pd.DataFrame(sf.describe()['sobjects'])

entitiyList = {}
for index,row in dfObjects.iterrows():
    entitiyList[row['name']] = row['label']

#Attributes for Dataframe
attributecolumnsrec = "byteLength,length,calculatedFormula,filteredLookupInfo,label,name,referenceTo,relationshipName,type".split(',')
attributecolumnsChildRelationships = "entityName,entityDesc,childSObject,field,relationshipName".split(',')

#Output List for Dataframe
entityRecordOutput = []
entityRecordChildRelationshipOutput = []

for entityName in entitiyList:
    #Entity properties
    entity = SFType(entityName, sf_instance=instance, session_id=session_id)
    entityDict = entity.describe()
    #Entity Attributes
    entityDictFieldsData = entity.describe()['fields']

    for rowFieldsData in entityDictFieldsData:
        recordx = {}
        recordx['entityName'] = entityName
        recordx['entityDesc'] = entitiyList[entityName]
        for attrval in attributecolumnsrec:
            recordx[attrval] = rowFieldsData[attrval]

        entityRecordOutput.append(recordx)

    #Child Relationships
    for key in entityDict:
        if key == 'childRelationships':
            for line in entityDict[key]:
                entityRecordChildRelationshipOutput.append([entityName,entitiyList[entityName],line['childSObject'],line['field'],line['relationshipName']])

#Saving list of entities with all the attributes from salesforce
dfObjects.to_csv(os.path.join(targetFolder,'salesforce_enitites' + '_out.tsv'),header=True, sep='\t', index=False)

#All the attributes and relevent fields for entities/objects
dfall = pd.DataFrame(entityRecordOutput)
dfall.to_csv(os.path.join(targetFolder, 'salesforce_enitites_attributes' + '_out.tsv'),sep='\t',header=True, index=False)

#Child relationships
dfall = pd.DataFrame.from_records(entityRecordChildRelationshipOutput,columns=attributecolumnsChildRelationships)
dfall.to_csv(os.path.join(targetFolder,'salesforce_enitites_childRelationship' + '_out.tsv'),sep='\t',header=True, index=False)
