import glob
import os
import csv
from scipy import stats

"""
Get latest file with filopodia lengths over time
"""
list_of_files = glob.glob('../filoLengthFiles/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

"""
Store file name and content
"""
fileName = latest_file.replace(".txt", "")
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
Get lists of extension and retraction times
"""
timePerExtPerFilo = []
timePerRetPerFilo = []
extDuration = extendedLength = retDuration = retractedLength = 0

for filo, lengths in lengthsPerFilo.items(): 
    # Only parse this filo's lengths if it has retracted fully, i.e. last length is 0
    if lengths[-1] != 0:
        continue
    # Can't use len(filo) for some reason: "'float' object is not callable" error 
    prev = 0
    for length in lengths:
        diff = length - prev
        if diff > 0.05: # EXTENSION. Note: I look for >0.05 difference because the model tends to produce some 0.04xx difference numbers which wouldnt actually be recorded in real life as it's very small to the human eye
            extDuration += TIME_STEP
            extendedLength += diff
        elif diff < 0: # RETRACTION
            retDuration += TIME_STEP
            retractedLength += abs(diff)
        prev = length

    # For this filo, add seconds taken to extend each micron. Do the same for retraction.
    timePerExtPerFilo.append(extDuration / extendedLength)
    # DEBUGGING
    if extDuration / extendedLength > 65:
        print ("ext", filo, extDuration, extendedLength)
    if retractedLength > 0:
        timePerRetPerFilo.append(retDuration / retractedLength)
        # DEBUGGING
        if retDuration / retractedLength > 90:
            print ("ret", filo, retDuration, retractedLength)

    # Reset values for next filo
    extDuration = extendedLength = retDuration = retractedLength = 0

"""
Get KS statistic for extension and retraction times
"""
# Retrieve invivo data
extTimesIV = []
retTimesIV = []

with open('extTimesIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line:
            extTimesIV.append(value)

with open('retTimesIV.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for line in reader:
        for value in line: 
            retTimesIV.append(value)

ksExt = stats.ks_2samp(timePerExtPerFilo, extTimesIV)
ksRet = stats.ks_2samp(timePerRetPerFilo, retTimesIV)
print(ksExt)
print(ksRet)
