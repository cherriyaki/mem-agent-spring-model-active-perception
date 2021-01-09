import csv
import numpy as np

lengthsPerFiloIV = []
with open('lengthsOverTimeIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    filoCtr = 0
    firstLine = True
    lengthsPerFiloIV = []
    for line in reader:
        for length in line:
            if firstLine: lengthsPerFiloIV.append([])
            lengthsPerFiloIV[filoCtr].append(length)
            filoCtr += 1
        firstLine = False
        filoCtr = 0

timePerExtPerFiloIV = []
timePerRetPerFiloIV = []
extDurationIV = extendedLengthIV = retDurationIV = retractedLengthIV = 0
TIME_STEP_IV = 30
for filo in lengthsPerFiloIV:
    # ""'float' object is not callable" error on doing len(filo) for some reason ??
    prev = 0
    for length in filo:
        diff = length - prev
        if diff > 0.: # extension
            extDurationIV += TIME_STEP_IV
            extendedLengthIV += diff
        elif diff < 0: # retraction
            retDurationIV += TIME_STEP_IV
            retractedLengthIV += abs(diff)
        prev = length
    # For this filo, add seconds taken to extend each micron. Do the same for retraction.
    timePerExtPerFiloIV.append(extDurationIV / extendedLengthIV)
    timePerRetPerFiloIV.append(retDurationIV / retractedLengthIV)
    # Reset values for next filo
    extDurationIV = extendedLengthIV = retDurationIV = retractedLengthIV = 0

extArr = np.asarray(timePerExtPerFiloIV)
retArr = np.asarray(timePerRetPerFiloIV)
np.savetxt("extTimesIV.csv", extArr, fmt='%.3f', delimiter=',')
np.savetxt("retTimesIV.csv", retArr, fmt='%.3f', delimiter=',')