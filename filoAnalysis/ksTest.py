import os
import invivoMetrics as iv
from scipy import stats
from analysisFunctions import getFiloMetrics
import subprocess
import sched, time

#TODO might need to make file param or sth
user = "limc"
jobId = None

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
    # os.system(f"./springAgent 1 0.9 0.04 2 {params[0]} {params[1]} 1 {params[2]} {params[3]} -1 -1")
    os.system("./springAgent 1 0.9 0.04 2 %f %f 1 %i %f -1 -1" % (params[0], params[1], params[2], params[3]))
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
        if line.strip() not in ['\n', '\r\n', '']: 
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
    return {"maxLen": ksMaxLen.statistic, "averageExtendingTime": ksAvgExt.statistic, "averageRetractingTime": ksAvgRet.statistic, "timeAtMax": ksTimeAtMax.statistic}


