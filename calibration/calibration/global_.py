import os, sys
from inspect import getframeinfo
import math
import numpy as np

TIME_STEP = 15
DEFAULTS = [1, 0.9, 0.04, 2, 2, 15, 1, 2, 512, 0.95, 0.1, -1, -1]
INDEXES = {
    "runNum": 0,
    "epsilon": 1,
    "VconcST": 2,
    "gradientType": 3,
    "filVary": 4,
    "filTipMax": 5,
    "tokenStrength": 6,
    "filSpacing": 7,
    "actinMax": 8,
    "filSpringC": 9,
    "filSpringL": 10,
    "randFilExtend": 11,
    "randFilRetract": 12
}
TYPES = ["int","float","float","int","float","float","float","int","float","float","float","float","float"]

RUNFILE = {
    "filVary": "filvary_", 
    "epsilon": "epsilon_",
    "VconcST": "VconcST",
    "gradientType": "GRADIENT",
    "filTipMax": "FILTIPMAX",
    "tokenStrength": "tokenStrength",
    "filSpacing": "FILSPACING",
    "actinMax": "actinMax",
    "filSpringC": "filSpringC",
    "filSpringL": "filSpringL",
    "randFilExtend": "randFilExtend",
    "randFilRetract": "randFilRetract",
    "runNum": "run"
}

def truncate(f, n):
    """
    @param f - positive float, n - number of digits to keep 
    """
    f = str(f)
    res = ""
    ct = 0   # digit count
    for c in f:
        if c != '.':
            ct += 1
        if ct > n:  # stop after we have parsed n digits
            break
        res += c
    return float(res)

def dimension(npArr):
    """
    takes a Numpy array and returns the number of dimensions
    """
    shape = npArr.shape
    return len(shape)

def fileName(f):
    """
    @param pass in __file__
    """
    return os.path.basename(f)

def lineNo(curFrame):
    """ 
    @param curFrame: the object returned by calling inspect.currentframe()
    """
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

