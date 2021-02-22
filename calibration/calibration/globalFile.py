import os, sys
from inspect import getframeinfo

TIME_STEP = 15

defaultAgentParams = None
outputFileNameFormat = None

def lineNo(curFrame):
    return getframeinfo(curFrame).lineno

def getRoot():
    cwd = os.getcwd()
    parts = _splitall(cwd)
    root = parts[0]
    for part in parts[1:]:
        if part == "calibration":
            break
        else:
            root = os.path.join(root, part)
    return root

# Thanks to https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html for this code
def _splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

