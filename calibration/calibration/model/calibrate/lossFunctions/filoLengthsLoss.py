from .lossFunction import LossFunction
from calibration import globalFile
from calibration.model import logWriter
import os
import csv
import traceback
from scipy import stats
from inspect import currentframe

class FiloLengthsLoss(LossFunction):
    def __init__(self, id_, paramNames):
        super().__init__(id_, paramNames, "filo_lengths")
        self.maxLosses = {"maxLen": 1, "averageExtendingTime": 1, "averageRetractingTime": 1, "timeAtMax": 1}

    def getLosses(self, candidate):
        """
        @param  candidate: [paramValue1, paramValue2, ...]
        @return {"obj1": loss, "obj2": loss, ...}
        """
        super().runAgent(candidate)
        output = super().getOutputContent(candidate, runOutputDir="filoLengthFiles")
        if output.strip() in ['\n', '\r\n', '']:    # Empty file: treat as no filopodia growth
            return self.maxLosses
        # TEST
        # print(output)
        # return self.maxLosses
        lengthsPerFilo = self._splitByFilo(output)
        featureDistributions = self._getFeatureDistri(lengthsPerFilo)
        return self._getKsValues(featureDistributions)        

    def _splitByFilo(self, content):
        """
        @return {filo1: [], filo2: []}
        """
        lengthsPerFilo = {}
        lines = content.split("\n")
        ctr = 0
        for line in lines:
            ctr += 1
            if line.strip() not in ['\n', '\r\n', '']: 
                elements = line.split(",")
                filo = elements[0]
                length = float(elements[1])
                if filo not in lengthsPerFilo: 
                    lengthsPerFilo[filo] = []
                lengthsPerFilo[filo].append(length) 
        return lengthsPerFilo

    def _getFeatureDistri(self, lengthsPerFilo):
        """
        @return {obj1: [], obj2: []}
        """
        extractor = FeaturesExtractor(self.id, globalFile.TIME_STEP)
        distri = extractor.getFeatureDistri(list(lengthsPerFilo.values()))
        logWriter.write(id=self.id, line=["DEBUG", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Got distributions for each objective"])
        return distri

    def _getKsValues(self, distributions):
        iv = self._getInvivo()
        ksMaxLen = stats.ks_2samp(distributions["maxLen"], iv["maxLen"])
        ksAvgExt = stats.ks_2samp(distributions["averageExtendingTime"], iv["averageExtendingTime"])
        ksAvgRet = stats.ks_2samp(distributions["averageRetractingTime"], iv["averageRetractingTime"])
        ksTimeAtMax = stats.ks_2samp(distributions["timeAtMax"], iv["timeAtMax"])
        return {"maxLen": ksMaxLen.statistic, "averageExtendingTime": ksAvgExt.statistic, "averageRetractingTime": ksAvgRet.statistic, "timeAtMax": ksTimeAtMax.statistic}

    def _getInvivo(self):
        """
        @return {obj1: [], obj2: []}
        """
        iv = InVivoData(self.id)
        return iv.getIVData()
  
class FeaturesExtractor:
    def __init__(self, id_, timeStep):
        self.id = id_
        self.MIN_MAX_LEN = 1
        self.TIME_STEP = timeStep
        self.maxLengths = []
        self.avgExtTimes = []
        self.timesAtMax = []
        self.avgRetTimes = []

        self.maxLen = 0
        self.timeTilMax = 0
        self.timeAtMax = 0
        self.timeTilZero = 0
        self.maxLenReached = False


    def getFeatureDistri(self, lengthsPerFilo):
        """
        @param: [[filo lengths], [filo lengths]]
        @return: {obj1: [], obj2: []}
        """
        self._addToDistributions(lengthsPerFilo)
        return self._getOutput()

    def _addToDistributions(self, lengthsPerFilo):
        for lengths in lengthsPerFilo:
            indivFilos = self._breakIntoFilos(lengths)  # The same pointer might have pointed to multiple filo objects
            for filo in indivFilos:
                if lengths[-1] != 0:    # Only parse this filo if it has retracted fully, i.e. last length is 0
                    continue
                maxLenAcceptable = self._getMaxLen(filo)
                if not maxLenAcceptable:   # If the max length reached is too small, then do not record this filopodium
                    continue
                self._resetValues()
                # For each length in this filo
                prev = 0
                for length in filo:
                    self._analyseLength(length, prev)
                    prev = length
        if not self.maxLengths or not self.avgExtTimes or not self.timesAtMax or not self.avgRetTimes:  # one of distri is empty
            logWriter.write(id=self.id, line=["ERROR", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"≥1 objective's distribution is empty. Might be that 0 filopodia retracted fully"])

    def _breakIntoFilos(self, list_):
        """
        @param [lengths belonging to a filo pointer]
        @return [[indiv filo lengths] [indiv filo lengths]]
        """
        individualFilopodia = []
        for i in range(len(list_)):
            # Start a new list of lengths if we are on the first index or the previous length is 0
            if i==0 or (list_[i] > 0 and list_[i-1]==0):
                individualFilopodia.append([])
            individualFilopodia[-1].append(list_[i])
        return individualFilopodia

    def _getMaxLen(self, filo):
        """
        If maxLen is not too small, then add it to the corresponding distribution
        """
        maxLen = max(filo)
        self.maxLen = maxLen
        maxLenAcceptable = maxLen >= self.MIN_MAX_LEN
        if maxLenAcceptable:
            self.maxLengths.append(maxLen)
        return maxLenAcceptable

    def _resetValues(self):
        self.timeTilMax = 0
        self.timeAtMax = 0
        self.timeTilZero = 0
        self.maxLenReached = False

    def _analyseLength(self, length, prev):
        if length < self.maxLen and not self.maxLenReached: # Filo has not reached its max length 
            self.timeTilMax += self.TIME_STEP
        elif length == self.maxLen and not self.maxLenReached:  # Filo is at its max length for the first time
            self.timeTilMax += self.TIME_STEP
            self.avgExtTimes.append(self.timeTilMax/self.maxLen)
            self.maxLenReached = True
        elif length == self.maxLen and self.maxLenReached:  # Filo has previously reached max length and is still on it
            self.timeAtMax += self.TIME_STEP
        elif length < self.maxLen and prev == self.maxLen:  # Filo has just started to retract
            self.timesAtMax.append(self.timeAtMax)
        
        if length < self.maxLen and length > 0 and self.maxLenReached:  # Filo has not fully retracted
            self.timeTilZero += self.TIME_STEP
        elif length == 0 and prev > 0:  # Filo has just completely retracted
            self.timeTilZero += self.TIME_STEP
            self.avgRetTimes.append(self.timeTilZero/self.maxLen)

    def _getOutput(self):
        return {
            "maxLen": self.maxLengths,
            "averageExtendingTime": self.avgExtTimes,
            "averageRetractingTime": self.avgRetTimes,
            "timeAtMax": self.timesAtMax
        }

class InVivoData:
    def __init__(self, id_):
        self.id = id_
        self.ivDir = os.path.join(globalFile.getRoot(), "calibration/data/filoLengths/invivo")
        self.maxLensIV = []
        self.avgExtIV = []
        self.avgRetIV = []
        self.timeAtMaxIV = []

    def getIVData(self):
        """
        @return {obj1: [], obj2: []}
        """
        self._fillLists()
        return self._createDict()

    def _createDict(self):
        """
        @return {obj1: [], obj2: []}
        """
        return {
            "maxLen": self.maxLensIV,
            "averageExtendingTime": self.avgExtIV,
            "averageRetractingTime": self.avgRetIV,
            "timeAtMax": self.timeAtMaxIV
        }
        

    def _fillLists(self):
        """
        Fill the lists for each objective with invivo data
        """
        self.maxLensIV = self._getData(self._path('maxLensIV.csv'))
        self.avgExtIV = self._getData(self._path('avgExtIV.csv'))
        self.avgRetIV = self._getData(self._path('avgRetIV.csv'))
        self.timeAtMaxIV = self._getData(self._path('timeAtMaxIV.csv'))
        logWriter.write(id=self.id, line=["DEBUG", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Loaded invivo data"])

    def _path(self, fileName):
        return os.path.join(self.ivDir, fileName)

    def _getData(self, file):
        """
        Return array of data from given csv
        """
        arr = []
        try:
            with open(file, encoding='utf-8-sig', newline='') as f:
                reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
                for line in reader:
                    for value in line:
                        arr.append(value)
        except:
            tb = traceback.format_exc()
            logWriter.write(id=self.id, line=["ERROR", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Invivo retrieval: Failed to open {file}"])
            logWriter.write(id=self.id, exc=tb)
            raise
        return arr

        

if __name__ == "__main__":
    loss = FiloLengthsLoss(1, ["filVary", "filSpacing"])
    loss._runAgent([1,1])