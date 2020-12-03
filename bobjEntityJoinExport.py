import pandas as pd
import glob

"""
bobjEntityJoinExport
-------------------------------------------------
        
General Information
-------------------------------------------------
            
    Data bobjEntityJoinExport
    -------------------------------------------------
    Data Foundation for bobjEntityJoinExport Universe.
Initial version created on 11-Sep-2017.
    File Name : bobjEntityJoinExport.dfx
    Modified : date time of the last save
            
        Statistics : 
            List of Values : 2
            Parameter : 3
            Table : 49
            Alias Table : 39
            Derived Table : 1
            Standard Table : 9
            Join : 30
            Context : 0
            View : 2
            TOTAL : 88
            
    Properties : 
        Allow Cartesian Products : :false
        Multiple SQL statements for each context : :true
        
Joins (30)
-------------------------------------------------
            
    Join
    -------------------------------------------------
    "WEB"."EVENT_NUMBER"="EVENTDESC"."EVENT_NUMBER"
and "WEB"."DAY_NUMBER"="DAYS"."DAY_NUMBER"

        
Tables (39)
-------------------------------------------------
            
    Table: WEB
    -------------------------------------------------
    WEB_EVENTS_DATA

    Table: DAYS
    -------------------------------------------------
    DAYS_DATA

    Table: EVENTDESC
    -------------------------------------------------
    EVENTDESC_DATA

    Derived Table: First Event
    -------------------------------------------------
    first event that is mapped to the user

        
Views (3)
-------------------------------------------------
            
    View: Master
    -------------------------------------------------
            
    View: Dimensions
    -------------------------------------------------
    
            
    View: Fact
    -------------------------------------------------
"""

basefolder = './data/bobj/'
infolder = basefolder + 'in/'
outfolder = basefolder + 'out/'
combineJoinTableAll = []

def cleanCount(row):
    return row.split(' ')[1].replace('(','').replace(')','')

def tableTypeClassification(tableName):
    tableName = tableName.upper().strip()
    if tableName.find('DIM_')> -1 :
        type = 'Dim'
    elif tableName.find('FCT') > -1:
        type = 'Fact'
    elif tableName.find('STG') > -1:
        type = 'Stg'
    elif tableName.find('HIST') > -1:
        type = 'History'
    elif tableName.find('AGG') > -1:
        type = 'Agg'
    else:
        type = 'Table'

    return type


#Getting the list of all the input file with .txt as extension
filelist = glob.glob(infolder+ '*.txt')

for BobJFullfilename in filelist:
    print(BobJFullfilename)
    BobJfilename = BobJFullfilename.split('/')[-1]
    BobJfilename = BobJfilename.split('.')[0]

    with open('{basefolder}{filename}.txt'.format(filename=BobJfilename,basefolder=infolder)) as f:
        rows = f.readlines()

        joinCount = tableCount = viewCount = 0
        joinSection = tableSection = viewSection = False
        tables = [] ; joins = [] ; views = []
        tableNamefound = joinfound = False
        tableName = tableType = joinStatement = ''

        for index,row in enumerate(rows):
            row = row.strip()
            if row == '-------------------------------------------------' or row == '' : continue

            if row.startswith('Joins'):
                joinSection = True
                tableSection = viewSection = False
                joinCount =  cleanCount(row)
            elif row.startswith('Tables'):
                tableSection = True
                joinSection = viewSection = False
                tableCount = cleanCount(row)
            elif row.startswith('Views'):
                viewSection = True
                joinSection = tableSection = False
                viewCount = cleanCount(row)

            # Table Processing

            if row.split(':')[0] in ['Table', 'Derived Table'] and tableName == '':

                tableType = row.split(':')[0].strip()
                tableName = row.split(':')[1].strip()

                if len(tableName.split(' - '))> 1:
                    tableType = tableName.split(' - ')[0].strip()
                elif tableType == 'Derived Table':
                    pass
                else:
                    tableType = tableTypeClassification(tableName)

                if rows[index + 2].strip() != '' :
                    tableNamefound = True
                else:
                    tables.append([BobJfilename,tableType, tableName.strip(), ''])
                    tableName = dbtableName = tableType = ''

            elif tableNamefound and tableName != '':
                dbtableName = row
                if tableType == 'Table':
                    tableType = tableTypeClassification(dbtableName)

                tables.append([BobJfilename,tableType,tableName.strip(),dbtableName.strip()])
                tableName = dbtableName = tableType = ''
                tableNamefound = False

            # Join processing

            if row.startswith('Join') and not row.startswith('Joins')  and joinStatement == '':

                takeOutJoin = row.replace('Join','').strip()
                joinStatement = takeOutJoin
                # print(row,joinStatement)

                if takeOutJoin != '':
                    joins.append([re.sub('\s+', ' ', joinStatement.replace('=', ' = '))])
                    joinStatement = ''
                    joinfound = False
                else:
                    joinStatement = ''
                    joinfound = True

            elif joinfound:

                if row.split(' ')[0].lower() in ['and', 'or']: row = ' '+ row

                joinStatement += row

                if rows[index + 1].strip() == '':
                    joins.append([re.sub('\s+',' ',joinStatement.replace('=',' = '))])
                    joinStatement = ''
                    joinfound = False

        # print(BobJfilename)
        tablesDf = pd.DataFrame.from_records(tables,columns=['universe','type','bobjEntity','dbtable'])
        joinsDf = pd.DataFrame.from_records(joins,columns=['join'])
        tablesDf.to_csv(outfolder+BobJfilename+'_tables.tsv',header=True,sep='\t',index=False )
        joinsDf.to_csv(outfolder + BobJfilename + '_joins.tsv', header=True, sep='\t', index=False)

        # print(tables)
        # print(joins)
        combineJoinTable = []
        for row in tables:
            tableName = row[2].upper()
            tableNameJoins = []

            for joinrows in joins:
                # print(joinrows)
                if re.findall(tableName, joinrows[0].replace('"','').upper()):
                    tableNameJoins.append(joinrows)
            # print(tableNameJoins)
            combineJoinTable.append([row[0],row[1],tableName,row[3],tableNameJoins])

        combineJoinTableAll.extend(combineJoinTable)
    # print(combineJoinTable)
tablesDfJoins = pd.DataFrame.from_records(combineJoinTableAll, columns=['universe','type', 'bobjEntity', 'dbtable','Joins'])
tablesDfJoins.to_csv(outfolder  + 'ALL_tablesWithJoins.tsv', header=True, sep='\t', index=False)
