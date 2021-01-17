import glob
import os
import csv
from scipy import stats
from analysisFunctions import getFiloMetrics

"""
Get latest file with filopodia lengths over time
"""
list_of_files = glob.glob('../filoLengthFiles/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

"""
Store file name and content
"""
fileName = latest_file.split('/')[2].replace(".txt", "")
f = open(latest_file, "r")
content = f.read()
f.close()

"""
CONSTANTS
"""
TIME_STEP = 15

"""
Get lengths recorded for each filopodium
"""
lengthsPerFilo = {}
# Get list of lengths for each filo
lines = content.split("\n")
for line in lines:
    if line != '': 
        elements = line.split(",")
        filo = elements[0]
        length = float(elements[1])
        if filo not in lengthsPerFilo: 
            lengthsPerFilo[filo] = []
        lengthsPerFilo[filo].append(length) 

# Quit this script if file is empty
if len(lengthsPerFilo) == 0:
    exit()

"""
Get lists for each metric
"""
metrics = getFiloMetrics(list(lengthsPerFilo.values()), TIME_STEP)

maxLenArr = metrics["maxLen"]
avgExtTimeArr = metrics["averageExtendingTime"]
avgRetTimeArr = metrics["averageRetractingTime"]
timeAtMaxArr = metrics["timeAtMax"]
extArr = metrics["timePerExtension"]
retArr = metrics["timePerRetraction"]

"""
Retrive invivo distributions for each metric
"""
maxLensIV = []
avgExtIV = []
avgRetIV = []
timeAtMaxIV = []
extTimesIV = []
retTimesIV = []

with open('invivo/maxLensIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line:
            maxLensIV.append(value)
with open('invivo/avgExtIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line:
            avgExtIV.append(value)
with open('invivo/avgRetIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line:
            avgRetIV.append(value)
with open('invivo/timeAtMaxIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line:
            timeAtMaxIV.append(value)
with open('invivo/extTimesIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line:
            extTimesIV.append(value)
with open('invivo/retTimesIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line: 
            retTimesIV.append(value)

"""
Get KS statistic for extension and retraction times
"""
ksMaxLen = stats.ks_2samp(maxLenArr, maxLensIV)
ksAvgExt = stats.ks_2samp(avgExtTimeArr, avgExtIV)
ksAvgRet = stats.ks_2samp(avgRetTimeArr, avgRetIV)
ksTimeAtMax = stats.ks_2samp(timeAtMaxArr, timeAtMaxIV)
ksExt = stats.ks_2samp(extArr, extTimesIV)
ksRet = stats.ks_2samp(retArr, retTimesIV)
print(ksExt)
print(ksRet)
