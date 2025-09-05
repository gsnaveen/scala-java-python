import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Copy S3 file for a date')
parser.add_argument('--file', dest='filename', type=str, help='Name of the File')
parser.add_argument('--colnum', dest='numCols', type=int, help='Number of columns in file')

args = parser.parse_args()
print(args.filename)
print(args.numCols)

sourcefile = args.filename

cleanFileName = sourcefile + '_clean'
errorFileName = sourcefile + '_error'

numCols = args.numCols

cleanFile = open(cleanFileName,"x")
errorFile = open(errorFileName,"x")
rowcount = defaultdict(int)
rows = clean = error = 0
with open(sourcefile) as file:

    for line in file:
        rows += 1
        # print(line.split('\t')[3])
        rowcount[len(line.split('\t'))] += 1
        if len(line.split('\t')) == numCols:
            clean += 1
            cleanFile.write(line)
        else:
            error += 1
            # print(line)
            errorFile.write(line)

cleanFile.close()
errorFile.close()

print("Total Rows = {rows} \nClean Rows = {clean} \nError Rows = {error}".format(rows=rows,clean=clean,error=error))
print(rowcount)
