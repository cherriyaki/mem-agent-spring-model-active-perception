import csv
import numpy as np
from analysisFunctions import getFiloMetrics

lengthsPerFiloIV = []
with open('filoAnalysis/invivo/lengthsOverTimeIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    filoCtr = 0
    firstLine = True
    for line in reader:
        for length in line:
            if firstLine: lengthsPerFiloIV.append([])
            lengthsPerFiloIV[filoCtr].append(length)
            filoCtr += 1
        firstLine = False
        filoCtr = 0

"""GET METRICS"""
TIME_STEP_IV = 30
metrics = getFiloMetrics(lengthsPerFiloIV, TIME_STEP_IV)

"""SAVE METRIC DISTRIBUTIONS TO FILES"""
maxLenArr = np.asarray(metrics["maxLen"])
avgExtTimeArr = np.asarray(metrics["averageExtendingTime"])
avgRetTimeArr = np.asarray(metrics["averageRetractingTime"])
timeAtMaxArr = np.asarray(metrics["timeAtMax"])
extArr = np.asarray(metrics["timePerExtension"])
retArr = np.asarray(metrics["timePerRetraction"])

np.savetxt("filoAnalysis/invivo/maxLensIV.csv", maxLenArr, fmt='%.3f', delimiter=',')
np.savetxt("filoAnalysis/invivo/avgExtIV.csv", avgExtTimeArr, fmt='%.3f', delimiter=',')
np.savetxt("filoAnalysis/invivo/avgRetIV.csv", avgRetTimeArr, fmt='%.3f', delimiter=',')
np.savetxt("filoAnalysis/invivo/timeAtMaxIV.csv", timeAtMaxArr, fmt='%.3f', delimiter=',')
np.savetxt("filoAnalysis/invivo/extTimesIV.csv", extArr, fmt='%.3f', delimiter=',')
np.savetxt("filoAnalysis/invivo/retTimesIV.csv", retArr, fmt='%.3f', delimiter=',')

