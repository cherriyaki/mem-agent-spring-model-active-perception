import csv
import os

def getIVdir():
    thisPath = os.path.dirname(__file__)
    path = os.path.join(thisPath, '../filoAnalysis/invivo/')
    return path

def getInVivoData(path):
    arr = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for line in reader:
            for value in line:
                arr.append(value)
    return arr

maxLensIV = getInVivoData(os.path.join(getIVdir(),'maxLensIV.csv'))
avgExtIV = getInVivoData(os.path.join(getIVdir(),'avgExtIV.csv'))
avgRetIV = getInVivoData(os.path.join(getIVdir(),'avgRetIV.csv'))
timeAtMaxIV = getInVivoData(os.path.join(getIVdir(),'timeAtMaxIV.csv'))

