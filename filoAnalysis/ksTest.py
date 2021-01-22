import os
import invivoMetrics as iv
from scipy import stats
from analysisFunctions import getFiloMetrics

""""""
def getKsValues(params):
    TIME_STEP = 15
    runAgent(params)
    content = getOutputContent(params)
    # TODO ensure content isn't empty
    lengthsPerFilo = getListsOfLengths(content)
    metrics = getFiloMetrics(list(lengthsPerFilo.values()), TIME_STEP)
    return getArrayOfKsValues(metrics)
    
def runAgent(params):
    os.system("./buildSpringAgent.sh --analysis \"filo_lengths\"")
    os.system(f"./springAgent 1 0.9 0.04 2 {params[0]} {params[1]} 1 {params[2]} {params[3]} -1 -1")

def getOutputContent(params):
    fileName = "filo_lengths_filvary_%f_epsilon_0.900000_VconcST0.040000_GRADIENT2_FILTIPMAX%f_tokenStrength1.000000_FILSPACING%i_actinMax%f_randFilExtend-1.000000_randFilRetract-1.000000_run_1_.txt" % (params[0],params[1],params[2],params[3])
    # # debug
    # print("CHERRY DEBUG filvary " + str(params[0]) + " filtipmax " + str(params[1]) + " filspacing " + str(params[2]) + " actinmax " + str(params[3]))
    fullPath = "filoLengthFiles" + os.sep + fileName
    f = open(fullPath, "r")
    content = f.read()
    f.close()
    return content

"""
Get lengths recorded for each filopodium
"""
def getListsOfLengths(content):
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

    return lengthsPerFilo

"""
Get KS statistics 
"""
def getArrayOfKsValues(metrics):
    ksMaxLen = stats.ks_2samp(metrics["maxLen"], iv.maxLensIV)
    ksAvgExt = stats.ks_2samp(metrics["averageExtendingTime"], iv.avgExtIV)
    ksAvgRet = stats.ks_2samp(metrics["averageRetractingTime"], iv.avgRetIV)
    ksTimeAtMax = stats.ks_2samp(metrics["timeAtMax"], iv.timeAtMaxIV)
    return [ksMaxLen.statistic, ksAvgExt.statistic, ksAvgRet.statistic, ksTimeAtMax.statistic]


