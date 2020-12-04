from pathlib import Path
import matplotlib.pyplot as plt
import math
import numpy as np
import os

# Get content of each file
fileToContent = {}
for path in Path("filoLengthFiles").iterdir():
    if path.is_file() and path.name.__contains__("filo"):
        f = open(path, "r")
        fileName = path.name.replace(".txt", "")
        content = f.read()
        fileToContent[fileName] = content
        f.close()

# Constants
TIME_STEP = 15
IMAGE_FOLDER = "filoLengthImages"
# make constants from invivo data?

"""
FOR EVERY FILE CONTAINING FILO LENGTHS
Each representing a run with specific parameters
"""
for file, content in fileToContent.items():
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

    # Skip this file if it is empty
    if len(lengthsPerFilo) == 0:
        continue

    """
    =========================================================
    CREATE FOLDER TO STORE IMAGES FOR THIS FILE
    """
    newFolder = IMAGE_FOLDER + "/" + file 
    if not os.path.exists(newFolder):
        try:
            os.mkdir(newFolder)
        except OSError:
            print ("Failed to create the directory %s failed" % newFolder)
        else:
            print ("Successfully created the directory %s " % newFolder)
    else:
        print ("Directory already exists: %s" % newFolder)
    
    """
    =========================================================
    GET EXTENSION AND RETRACTION RATES
    """

    timePerExtPerFilo = []
    timePerRetPerFilo = []
    extDuration = extendedLength = retDuration = retractedLength = 0

    for filo, lengths in lengthsPerFilo.items(): #lengths in lengthsPerFilo.values():
        # Only parse this filo's lengths if it has retracted fully, i.e. last length is 0
        if lengths[-1] != 0:
            continue
        # Can't use len(filo) for some reason: "'float' object is not callable" error 
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
        # DEBUGGING
        if extDuration / extendedLength > 65:
            print ("ext", filo, extDuration, extendedLength)
        # For time being we keep filos that don't retract in a run
        if retractedLength > 0:
            timePerRetPerFilo.append(retDuration / retractedLength)
            # DEBUGGING
            if retDuration / retractedLength > 90:
                print ("ret", filo, retDuration, retractedLength)

        # Reset values for next filo
        extDuration = extendedLength = retDuration = retractedLength = 0

    # FOR DEBUGGING
    print(max(timePerExtPerFilo))
    print(max(timePerRetPerFilo))

    """
    =========================================================
    HISTOGRAM
    """

    # make bin size 2. Aim: 0<x<=2s, 2<x<=4 ...
    extBins = math.ceil(max(timePerExtPerFilo)-min(timePerExtPerFilo)) *2
    retBins = math.ceil(max(timePerRetPerFilo)-min(timePerRetPerFilo)) *2

    # The one figure window which we will reuse to plot graphs, saving to an image each time
    fig = plt.figure()

    freqExtTime, extTimes, _ = plt.hist(timePerExtPerFilo, extBins, density=True) 
    # Labels
    plt.title("Histogram of extension rate")
    plt.xlabel("Seconds per extended micron")
    plt.ylabel("Probability")
    fig.savefig(newFolder + "/histogramExtRate.png")
    # Clears current fig
    plt.clf()

    freqRetTime, retTimes, _ = plt.hist(timePerRetPerFilo, retBins, density=True) 
    # Labels
    plt.title("Histogram of retraction rate")
    plt.xlabel("Seconds per retracted micron")
    plt.ylabel("Probability")
    fig.savefig(newFolder + "/histogramRetRate.png")
    # Clears current fig
    plt.clf()

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
    fig.savefig(newFolder + "/cdfExtRate.png")
    # Clears current fig
    plt.clf()

    plt.plot(retTimes[1:], cumSumRet)
    plt.title("CDF of retraction rate")
    plt.xlabel("Seconds per micron retracted")
    plt.ylabel("Cumulative probability")
    fig.savefig(newFolder + "/cdfRetRate.png")
    # Clears current fig
    plt.clf()

# CLOSE ENTIRE PLOT WINDOW
plt.close()


    

    
