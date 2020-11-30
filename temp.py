from pathlib import Path
import matplotlib.pyplot as plt
import math
import numpy as np

content = None
for path in Path("filoLengthFiles").iterdir():
    if path.is_file():
        f = open(path, "r")
        content = f.read()
        f.close()

lengthsPerFilo = {}

lines = content.split("\n")
for line in lines:
    if line != '': 
        elements = line.split(",")
        filo = elements[0]
        length = float(elements[1])
        if filo not in lengthsPerFilo: 
            lengthsPerFilo[filo] = []
        lengthsPerFilo[filo].append(length) 

"""
=========================================================
GET EXTENSION AND RETRACTION RATES
"""


timePerExtPerFilo = []
timePerRetPerFilo = []
extDuration = extendedLength = retDuration = retractedLength = 0
TIME_STEP = 30

for lengths in lengthsPerFilo.values():
    # ""'float' object is not callable" error on doing len(filo) for some reason ??
    prev = 0
    for length in lengths:
        diff = length - prev
        if diff > 0: # extension
            extDuration += TIME_STEP
            extendedLength += diff
        elif diff < 0: # retraction
            retDuration += TIME_STEP
            retractedLength += abs(diff)
        prev = length
    # For this filo, add seconds taken to extend each micron. Do the same for retraction.
    timePerExtPerFilo.append(extDuration / extendedLength)
    timePerRetPerFilo.append(retDuration / retractedLength)
    # Reset values for next filo
    extDuration = extendedLength = retDuration = retractedLength = 0

"""
=========================================================
HISTOGRAM
"""
extBins = math.ceil(max(timePerExtPerFilo)-min(timePerExtPerFilo)) *2
retBins = math.ceil(max(timePerRetPerFilo)-min(timePerRetPerFilo)) *2

freqExtTime, extTimes, _ = plt.hist(timePerExtPerFilo, extBins, density=True) 
# Labels
plt.title("Histogram of extension rate")
plt.xlabel("Seconds per extended micron")
plt.ylabel("Probability")

freqRetTime, retTimes, _ = plt.hist(timePerRetPerFilo, retBins, density=True) 
# Labels
plt.title("Histogram of retraction rate")
plt.xlabel("Seconds per retracted micron")
plt.ylabel("Probability")

"""
=========================================================
CUMULATIVE DISTRIBUTION
"""

cumSumExt = np.cumsum(freqExtTime) * (extTimes[1]-extTimes[0]) 
cumSumRet = np.cumsum(freqRetTime) * (retTimes[1]-retTimes[0])

plt.plot(extTimes[1:], cumSumExt)
plt.title("CDF of extension rate")
plt.xlabel("Seconds per micron extended")
plt.ylabel("Cumulative probability")

plt.plot(retTimes[1:], cumSumRet)
plt.title("CDF of retraction rate")
plt.xlabel("Seconds per micron retracted")
plt.ylabel("Cumulative probability")
