import os
import invivoMetrics as iv
from scipy import stats
from analysisFunctions import getFiloMetrics
import subprocess
import sched, time
import sys

#TODO might need to make file param or sth
user = "limc"
jobId = None
fullPath = ""
maxLosses = {"maxLen": 1, "averageExtendingTime": 1, "averageRetractingTime": 1, "timeAtMax": 1}

""""""
def getKsValues(params):
    TIME_STEP = 15
    runReturn = runAgent(params)
    if runReturn == 0:
        content = getOutputContent(params)
        # if content is empty, return maximum losses
        if content.strip() in ['\n', '\r\n', '']:
            return maxLosses
        lengthsPerFilo = getListsOfLengths(content)
        metrics = getFiloMetrics(list(lengthsPerFilo.values()), TIME_STEP)
        return getArrayOfKsValues(metrics)
    else:
        print("CHERRY DEBUG: agent didn't run | params = " + str(params))
        return maxLosses

def runAgent(params):
    root = getRoot()
    buildReturn = subprocess.call(f"{root}./buildSpringAgent.sh --analysis \"filo_lengths\"", shell=True)
    if buildReturn == 0:
        agentReturn = subprocess.call(f"{root}./springAgent 1 0.9 0.04 2 %f %f 1 %i %f -1 -1" % (params[0], params[1], params[2], params[3]), shell=True)
        return agentReturn
    else:
        print("cherry debug: agent didn't build")
        return 1
#     campScriptOutput = subprocess.check_output(f"./campScript.sh --analysis \"filo_lengths\" --runs 1 --vary1 filconstnorm \"{params[0]}\" --vary2 filtipmax \"{params[1]}\" --filspacing \"{params[2]}\" --actinmax \"{params[3]}\"")
#     jobId = subprocess.check_output(f"echo {campScriptOutput} | awk -F, '$1 == \"job_id\"{print $2}'")
#     s = sched.scheduler(time.time, time.sleep)
#     s.enter(60, 1, checkAgentFinished, (s,))
#     s.run()

# def checkAgentFinished(sc): 
#     os.system(f"ssh -Y {user}@login.camp.thecrick.org")
#     jobsOutput = subprocess.check_output()
#     s.enter(60, 1, checkAgentFinished, (sc,))

def getOutputContent(params):
    fileName = "filo_lengths_filvary_%f_epsilon_0.900000_VconcST0.040000_GRADIENT2_FILTIPMAX%f_tokenStrength1.000000_FILSPACING%i_actinMax%f_randFilExtend-1.000000_randFilRetract-1.000000_run_1_.txt" % (params[0],params[1],params[2],params[3])
    fullPath = os.path.join(getRoot(),"filoLengthFiles" + os.sep + fileName)
    try:
        f = open(fullPath, "r")
        content = f.read()
        f.close()
    except:
        print("cherry caught error: " + sys.exc_info()[0] + " | filename = " + fileName)
        content = ""
    return content

"""
Get lengths recorded for each filopodium
"""
def getListsOfLengths(content):
    lengthsPerFilo = {}
    # Get list of lengths for each filo
    lines = content.split("\n")
    ctr = 0
    for line in lines:
        ctr += 1
        if line.strip() not in ['\n', '\r\n', '']: 
            elements = line.split(",")
            filo = elements[0]
            try:
                length = float(elements[1])
                if filo not in lengthsPerFilo: 
                    lengthsPerFilo[filo] = []
                lengthsPerFilo[filo].append(length) 
            except:
                print("cherry CAUGHT ERROR " + sys.exc_info()[0] + " | line " + str(ctr) + ": '" + line + "' | file: " + fullPath)

    return lengthsPerFilo

"""
Get KS statistics 
"""
def getArrayOfKsValues(metrics):
    ksMaxLen = stats.ks_2samp(metrics["maxLen"], iv.maxLensIV)
    ksAvgExt = stats.ks_2samp(metrics["averageExtendingTime"], iv.avgExtIV)
    ksAvgRet = stats.ks_2samp(metrics["averageRetractingTime"], iv.avgRetIV)
    ksTimeAtMax = stats.ks_2samp(metrics["timeAtMax"], iv.timeAtMaxIV)
    return {"maxLen": ksMaxLen.statistic, "averageExtendingTime": ksAvgExt.statistic, "averageRetractingTime": ksAvgRet.statistic, "timeAtMax": ksTimeAtMax.statistic}

def getRoot():
    thisPath = os.path.dirname(__file__)
    root = os.path.join(thisPath, '../')
    return root

