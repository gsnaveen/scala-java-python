from modules.configs import *

def computeFixedHeader (header,split):
    headerSplit = header.split(split)
    startNumber = endNumber = 0

    headerLength = []
    for index,head in enumerate(headerSplit):
        lengthOfSplit = len(head)

        endNumber = startNumber + lengthOfSplit
        headerLength.append([index,startNumber , endNumber,head])
        # print(lengthOfSplit,[index,startNumber , endNumber],head)
        startNumber += lengthOfSplit
        startNumber += 1

    return headerLength

fileName = 'textdescdata'
inFile = BASEIN+fileName + '.txt'
outFile = BASEOUT+fileName + '_out.txt'
header = "|Material|Manufacturer                    |Brand                           |Model|"

headerLength = computeFixedHeader(header,'|')
SelectedCol = [1,9,11]
items = set()
with open(inFile) as inx:
    rows = inx.readlines()


    for index,row in enumerate(rows):
        Material = row[headerLength[1][1]:headerLength[1][2]]
        lmd  = row[headerLength[9][1]:headerLength[9][2]]
        materialShort = row[headerLength[11][1]:headerLength[11][2]]
        items.add(lmd)

    print(index,len(items))
    with open(outFile, 'w') as outx:
        for row in items:
            outx.write(row+'\n')

        # print(Material,lmd,materialShort)

        # if index == 10 : break
