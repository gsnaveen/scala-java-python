from modules.imports import *

"""
Business Layer
"""
test = True

if test:
    basefolder = './data/bobjfolders/'
    infolder = basefolder + 'test/'
    outfolder = basefolder + 'test/'
else:
    basefolder = './data/bobjfolders/'
    infolder = basefolder + 'in/'
    outfolder = basefolder + 'out/'

combinedAllData = []
FiltersListAll = []
def cleanCount(row):
    return row.split(' ')[1].replace('(','').replace(')','')


filelist = glob.glob(infolder+ '*.txt')

print(filelist)

for BobJFullfilename in filelist:
    # print(BobJFullfilename)
    BobJfilename = BobJFullfilename.split('/')[-1]
    BobJfilename = BobJfilename.split('.')[0]
    #Resetting for each file
    ObjectHier = []
    MeasureAttribute = []
    FiltersList = []
    SQLKey = False
    ObjectSection = MeasureAtterSection = FolderSelection = DimAttrSelection = FilterSelection = False
    measureHash = {}
    highestlevel = 1
    with open('{basefolder}{filename}.txt'.format(filename=BobJfilename,basefolder=infolder),'r',encoding='cp1252') as f:
        rows = f.readlines()

        # joinCount = tableCount = viewCount = 0
        # joinSection = tableSection = viewSection = False
        # tables = [] ; joins = [] ; views = []
        # tableNamefound = joinfound = False
        # tableName = tableType = joinStatement = ''
        x = 0

        for index,row in enumerate(rows):

            if row.startswith('Object layout'):
                ObjectSection = True
                MeasureAtterSection = FolderSelection = DimAttrSelection = FilterSelection = False
                level1 = ''
                level2 = ''
                level3 = ''
                level4 = ''
                level5 = ''
                level6 = ''
                level7 = ''
                level8 = ''

            elif row.startswith('Measures and Attributes'):
                MeasureAtterSection = True
                ObjectSection = FolderSelection = DimAttrSelection = FilterSelection = False

            elif row.startswith('Folders'):
                FolderSelection = True
                ObjectSection = MeasureAtterSection = DimAttrSelection = FilterSelection = False

            elif row.startswith('Dimensions and Attributes'):
                 DimAttrSelection = True
                 ObjectSection = MeasureAtterSection = FolderSelection = FilterSelection = False

            elif row.startswith('Filters'):
                FilterSelection = True
                ObjectSection = MeasureAtterSection = FolderSelection = DimAttrSelection = False


            if ObjectSection: #and x < 100:

                rowStrip = row.strip()
                if rowStrip == '-------------------------------------------------' or rowStrip == '': continue

                rowProcess = row.replace('    ','\t').rstrip('\n')
                ObjectLevels = rowProcess.split('\t')
                ObjectLevelsLen = len(ObjectLevels)
                # levelLen = max(levelLen,len(ObjectLevels))
                # print(ObjectLevels)

                if ObjectLevelsLen == 2 and ObjectLevels[1] != '':
                    level1 = ObjectLevels[1]
                    level2 = ''
                    level3 = ''
                    level4 = ''
                    level5 = ''
                    level6 = ''
                    level7 = ''
                    level8 = ''
                    highestlevel =1
                elif ObjectLevelsLen == 3 and ObjectLevels[2] != '':
                    level2 = ObjectLevels[2]
                    level3 = ''
                    level4 = ''
                    level5 = ''
                    level6 = ''
                    level7 = ''
                    level8 = ''
                    highestlevel=2
                elif ObjectLevelsLen == 4 and ObjectLevels[3] != '':
                    level3 = ObjectLevels[3]
                    level4 = ''
                    level5 = ''
                    level6 = ''
                    level7 = ''
                    level8 = ''
                    highestlevel=3
                elif ObjectLevelsLen == 5 and ObjectLevels[4] != '':
                    level4 = ObjectLevels[4]

                    level5 = ''
                    level6 = ''
                    level7 = ''
                    level8 = ''
                    highestlevel=4
                elif ObjectLevelsLen == 6 and ObjectLevels[5] != '':
                    level5 = ObjectLevels[5]

                    level6 = ''
                    level7 = ''
                    level8 = ''
                    highestlevel=5
                elif ObjectLevelsLen == 7 and ObjectLevels[6] != '':
                    level6 = ObjectLevels[6]

                    level7 = ''
                    level8 = ''
                    highestlevel = 6
                elif ObjectLevelsLen == 8 and ObjectLevels[7] != '':
                    level7 = ObjectLevels[7]

                    level8 = ''
                    highestlevel=7
                elif ObjectLevelsLen == 9 and ObjectLevels[8] != '':
                    level8 = ObjectLevels[8]
                    highestlevel = 8
                ObjectHier.append([BobJfilename,highestlevel,level1,level2,level3,level4,level5,level6,level7,level8])


            if MeasureAtterSection :
                row = row.strip()
                rowStrip = row.strip()
                if rowStrip == '-------------------------------------------------' or rowStrip == '': continue
                firstCollon = row.find(':')
                if firstCollon == -1:
                    mKey = ''
                else:
                    mKey = row[0:firstCollon].strip()

                mValue = row[firstCollon +1:].strip()

                if mKey == 'SQL Definition':
                    SQLKey = True

                if mKey == 'Measure':
                    measureDict = {'Measure':mValue,
                                   'businessName':'',
                                   'state': '',
                                   'dataType' :'',
                                   'access' : '',
                                   'forResult': '',
                                   'aggregationFunction':'',
                                   'highPrecision':'',
                                   'SQL Definition':'',
                                   'Can be used in':''

                    }
                    SQLKey = False
                    SqlStatement = ''
                    # ['Measure','businessName','state','dataType','access','forResult','aggregationFunction','highPrecision','SQL Definition','Can be used in']
                    # print("Starting Found")
                elif mKey == 'Can be used in':
                    measureDict['SQL Definition'] = SqlStatement
                    measureDict[mKey] = mValue
                    # MeasureAttribute.append(list(measureDict.values()))
                    listObjForMeasure = [
                                            BobJfilename,
                                            measureDict['Measure'],
                                            measureDict['businessName'],
                                            measureDict['state'],
                                            measureDict['dataType'],
                                            measureDict['access'],
                                            measureDict['forResult'],
                                            measureDict['aggregationFunction'],
                                            measureDict['highPrecision'],
                                            measureDict['SQL Definition'],
                                            measureDict['Can be used in']
                                             ]
                    measureHash[measureDict['Measure']] = listObjForMeasure
                    MeasureAttribute.append(listObjForMeasure)
                    # pp.pprint(measureDict)
                    # print(measureDict)
                    # print(MeasureAttribute)
                    # print("End Found")
                elif SQLKey: # Since SQL statement can be more than one line
                    if SqlStatement == '':
                        SqlStatement = mValue
                    else:
                        SqlStatement = SqlStatement + ' ' + row

                elif firstCollon > -1 and mKey != '':
                    if mKey in measureDict:
                        measureDict[mKey] = mValue


            if FilterSelection:

                row = row.strip()
                rowStrip = row.strip()
                if rowStrip == '-------------------------------------------------' or rowStrip == '': continue
                firstCollon = row.find(':')
                if firstCollon == -1:
                    mKey = ''
                else:
                    mKey = row[0:firstCollon].strip()

                mValue = row[firstCollon + 1:].strip()

                if mKey == 'Where expression':
                    SQLKey = True

                if mKey == 'Filter':

                    FilterDict = {'Filter': mValue,
                                   'Name' : '',
                                   'Path' : '',
                                   'State' : '',
                                   'Filter type': '',
                                   'forResult': '',
                                   'Where expression': ''
                                   }
                    SQLKey = False
                    SqlStatement = ''
                elif SQLKey: # Since SQL statement can be more than one line
                    if SqlStatement == '':
                        SqlStatement = mValue
                    else:
                        SqlStatement = SqlStatement + ' ' + row

                        if rows[index + 1].strip() == '':
                            FilterDict['Where expression'] = SqlStatement
                            SQLKey = False
                            SqlStatement = ''
                            FiltersList.append([
                                BobJfilename,
                                FilterDict['Filter'],
                                FilterDict['Name'],
                                FilterDict['Path'],
                                FilterDict['State'],
                                FilterDict['Filter type'],
                                FilterDict['Where expression']
                            ])

                elif firstCollon > -1 and mKey != '':
                    if mKey in FilterDict:
                        FilterDict[mKey] = mValue




                # 'Filter'
                # , 'Name'
                # , 'Path'
                # , 'State'
                # , 'Filter type'
                # , 'Where expression'


    def checkMeasure(row1,mDict=measureHash):
        returnVal = ['','','','','','','','','','','']
        rowlen = len(row1)
        for val in row1:
            if val != '' and val in mDict:
                returnVal = mDict.get(val)

        return returnVal

    for row in ObjectHier:
        measureReturned = checkMeasure(row)
        list3 = row + measureReturned
        combinedAllData.append(list3)

    FiltersListAll.extend(FiltersList)

    FiltersListDf = pd.DataFrame.from_records(FiltersList,
                                              columns=['universe',   'Filter', 'Name', 'Path', 'State', 'Filter type', 'Where expression'])
    FiltersListDf.to_csv(outfolder + BobJfilename +'_filters.tsv', header=True, sep='\t', index=False)

    MeasureAttributeDF = pd.DataFrame.from_records(MeasureAttribute,
                                              columns=['universe','Measure','businessName','state','dataType','access','forResult','aggregationFunction','highPrecision','SQL Definition','Can be used in'])
    MeasureAttributeDF.to_csv(outfolder + BobJfilename +'_folderMeasure.tsv', header=True, sep='\t', index=False)


    ObjectHierDF = pd.DataFrame.from_records(ObjectHier,
                                              columns=['universe', 'highestlevel','level1', 'level2', 'level3', 'level4','level5','level6','level7','level8'])
    ObjectHierDF.to_csv(outfolder + BobJfilename +'_folderHierarchy.tsv', header=True, sep='\t', index=False)

combinedAllDataDf =  pd.DataFrame.from_records(combinedAllData,
                                          columns=['universe', 'highestlevel','level1', 'level2', 'level3', 'level4','level5','level6','level7','level8','universe2','Measure','businessName','state','dataType','access','forResult','aggregationFunction','highPrecision','SQL Definition','Can be used in'])
combinedAllDataDf.to_csv(outfolder + 'ALL_Universe_data.tsv', header=True, sep='\t', index=False)

FiltersListAllDf = pd.DataFrame.from_records(FiltersListAll,
                                          columns=['universe', 'Filter', 'Name', 'Path', 'State', 'Filter type',
                                                   'Where expression'])
FiltersListAllDf.to_csv(outfolder + 'ALL_filters.tsv', header=True, sep='\t', index=False)

# Navigation Paths
# Queries
# List of Values
# Parameters
