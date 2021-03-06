import os,sys
import pandas as pd

basePath = "./mlData"
baseOutPath = "./mlOutData"
joinKey = ["customer"]
inData = os.listdir(basePath)
totalFiles = len(inData)

if totalFiles < 2:
    sys.exit("Not enough Files to merge")

toProcessFile = inData[0]
mainDataSet = pd.read_csv(basePath+"/"+toProcessFile,sep="\t",header='infer')

for i in range(1,totalFiles):
    toProcessFile = inData[i]
    nexttoProcessFile = pd.read_csv(basePath+"/"+toProcessFile,sep="\t",header='infer')
    mainDataSet = pd.merge(mainDataSet, nexttoProcessFile, on=joinKey,how='outer')
mainDataSet = mainDataSet.fillna(0)

mainDataSet.to_csv(baseOutPath+"/"+ "_".join(joinKey) +".txt",sep='\t',header=True, index=False)

'''
customer 	clicks 	downloads 	visits
 	A 	    10.0 	    0.0 	10.0
 	B 	    20.0 	    0.0 	20.0
 	C 	    30.0 	    0.0 	0.0
 	E 	    0.0 	    10.0 	0.0
 	F 	    0.0 	    20.0 	0.0
'''
