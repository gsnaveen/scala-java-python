import glob , os
import pandas as pd

basefolder = './data/csv/'

csvFileAttribute = []



for root, subFolder, files in os.walk(basefolder):
    for item in files:
        if item.endswith(".csv") :
            fileNamePath = str(os.path.join(root,item))
            print(fileNamePath)
            sourcebase = pd.read_csv(fileNamePath, header=0, sep=",")
            # print(list(sourcebase.columns))
            for col in list(sourcebase.columns):
                csvFileAttribute.append([fileNamePath.split('/')[-2],fileNamePath.split('/')[-1],col])

dfsummary = pd.DataFrame.from_records(csvFileAttribute,
                                      columns=["folder", "file", "column"])
dfsummary.to_csv(os.path.join(basefolder, 'csv' + '__' + "summaryTableColumns.tsv"), sep='\t',
                 index=False, header=True)
