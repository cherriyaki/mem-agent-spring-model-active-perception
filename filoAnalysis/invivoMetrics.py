import csv

def getInVivoData(path):
    arr = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for line in reader:
            for value in line:
                arr.append(value)
    return arr

maxLensIV = getInVivoData('filoAnalysis/invivo/maxLensIV.csv')
avgExtIV = getInVivoData('filoAnalysis/invivo/avgExtIV.csv')
avgRetIV = getInVivoData('filoAnalysis/invivo/avgRetIV.csv')
timeAtMaxIV = getInVivoData('filoAnalysis/invivo/timeAtMaxIV.csv')
