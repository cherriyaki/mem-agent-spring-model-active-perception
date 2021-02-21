import os, sys
from datetime import datetime
from calibration import globalFile

def main():
    args = _getArgDict()
    time = _getTimeStamp()
    line = _format(time, args)
    logFile = _getLogFile(args["ID"])
    try:
        with open(logFile, 'a') as f:       # open file in append mode
            f.write(line)
    except (IOError, OSError):
        print('could not open file ' + logFile)

def _getArgDict():
    return {
        "ID": sys.argv[1],
        "Type": sys.argv[2],
        "File": sys.argv[3],
        "Line": sys.argv[4],
        "Message": sys.argv[5]
    }

def _getTimeStamp():
    dateTimeObj = datetime.now()
    # ensure correct digits: YYYY-MM-DD hh:mm:ss
    return dateTimeObj.strftime('%Y-%m-%d') + ' ' + dateTimeObj.strftime('%H:%M:%S')

def _format(time, args):
    timeAndType = time + ' ' + args["Type"] + '\t'
    fileAndLine = args["File"] + ':' + args["Line"] + ' - '
    return timeAndType + fileAndLine + args["Message"] + '\n'

def _getLogFile(ID):
    root = globalFile.getRoot()
    logFile = os.path.join(root, f"calibration/logs/log_{ID}.log")
    return logFile

if __name__ == '__main__':
    main()