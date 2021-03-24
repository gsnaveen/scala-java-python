from modules.mongoConnect import *


for collection in dbCollections:
    dataOUT = []
    columns = set()
    collectionName = collection[1]
    if collectionName == 'collectionName':
        collection = mongoDB['collectionName']
        for row in collection.find({}):
            # print(collection)
            # print(row)
            mydict = {}
            parent = None
            flatten(parent, row, mydict)
            # print(list(mydict.keys()))
            dataOUT.append(mydict)
            columns.update(list(mydict.keys()))
            # print(row)
            # row = row
            # for key in row:
            #     if isinstance(key, dict):
            #         print(key)
            #     else:
            #         print(key)
            # break

    # print(len(dataOUT))
    # print(dataOUT)
    # print(columns)
    allData = []
    for row in dataOUT:
        rowData = []
        for col in columns:
            val = row.get(col, None)
            rowData.append(val)

        allData.append(rowData)

    targetFolder = os.path.join("./data", "mongoDB")
    df = pd.DataFrame.from_records(allData, columns=list(columns))
    df.to_csv(os.path.join(targetFolder, collectionName + '_tabs_out.tsv'), sep='\t', header=True, index=False)

    dfcolumnValues = pd.DataFrame()
    for col in columns:
        DfToSheet = df[[col]].astype(str).drop_duplicates().copy().reset_index()
        dfcolumnValues = dfcolumnValues.merge(DfToSheet, left_index=True, right_index=True, how='outer')
    dfcolumnValues[list(columns)].to_csv(os.path.join(targetFolder, collectionName + '_tabs_cols_out.tsv'), sep='\t', header=True, index=False)
