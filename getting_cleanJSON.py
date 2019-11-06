import json

def processLog(inList):
    startJSON = False
    OutData = []
    theJSONString = ''
    for row in inList:
        rowSplit = row.split('\n')
        for rowSplitVal in rowSplit:
            rowSplitVal = rowSplitVal.strip()
            if rowSplitVal == '' : continue

            if rowSplitVal.startswith('{'):
                startJSON = True

            if startJSON and rowSplitVal.endswith('}'):
                theJSONString += rowSplitVal
                OutData.append(json.loads(theJSONString))
                theJSONString = ''
                startJSON = False
            else:
                theJSONString += rowSplitVal

    return OutData



inList = ['\n\n\n{"myKey1":[1,2,3,4,',
          '5,6,7,8,',
          '9,10]}\n{"myKey1":[9,8,7]}']


print(processLog(inList))
