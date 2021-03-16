import os, sys
import argparse
from datetime import datetime
from calibration import global_

def w(**kwargs):
    """ @param id=ID, line=[messageType, currentFilename, lineNum, message], OR
    exc="exceptionTrace"
    Tip: exceptionTrace can be obtained by traceback.format_exc()
    """
    id_ = kwargs["id"]
    if "line" in kwargs:
        _writeLine(id_, kwargs["line"])
    elif "exc" in kwargs:
        _write(id_, kwargs["exc"])


def _writeLine(id_, arr):
    args = _getArgDict(arr)
    time = _getTimeStamp()
    line = _format(time, args)
    logFile = _getLogFile(id_)
    try:
        with open(logFile, 'a') as f:   # open file in append mode
            f.write(line)
    except (IOError, OSError):
        print('could not open file ' + logFile)

def _write(id_, str_):
    logFile = _getLogFile(id_)
    try:
        with open(logFile, 'a') as f:   # open file in append mode
            f.write(str_ + "\n")
    except (IOError, OSError):
        print('could not open file ' + logFile)

def _getArgDict(arr):
    return {
        "Type": arr[0],
        "File": arr[1],
        "Line": arr[2],
        "Message": arr[3]
    }

def _getTimeStamp():
    dateTimeObj = datetime.now()
    # ensure correct digits: YYYY-MM-DD hh:mm:ss
    return dateTimeObj.strftime('%Y-%m-%d') + ' ' + dateTimeObj.strftime('%H:%M:%S')

def _format(time, args):
    timeAndType = time + ' ' + args["Type"] + '\t'
    fileAndLine = args["File"] + ':' + str(args["Line"]) + ' - '
    return timeAndType + fileAndLine + args["Message"] + '\n'

def _getLogFile(id_):
    root = global_.getRoot()
    logFile = os.path.join(root, f"calibration/logs/{id_}.log")
    return logFile

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int)
    parser.add_argument('--line', action="extend", nargs="+", type=str)
    parser.add_argument('--exc', type=str)
    args = parser.parse_args()
    if args.line != None:
        # line = _separate(args.line)
        w(id=args.id, line=args.line)
    elif args.exc != None:
        w(id=args.id, exc=args.exc)
