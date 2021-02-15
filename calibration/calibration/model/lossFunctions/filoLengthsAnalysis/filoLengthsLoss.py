from ... import config
from .. import lossFunction.LossFunction

class FiloLengthLossFunction(LossFunction):
    def __init__(self):
        super(FiloLengthLossFunction, self).__init__("filo_lengths")

    def getLosses(self, candidate):
        self._runAgent(candidate)
        output = self._getOutputContent(candidate)
        lengthsPerFilo = self._splitByFilo(output)
        featureDistributions = self._getFeatureDistri(lengthsPerFilo)
        return self._getKsValues(featureDistributions)

    def _splitByFilo(self, content):
        pass

    def _getFeatureDistri(self, lengthsPerFilo):
        extractor = FeaturesExtractor(config.TIME_STEP)
        return extractor.getFeatureDistri

    def _getKsValues(self, featureDistributions):
        pass
  
class FeaturesExtractor:
    def __init__(self, timeStep):
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
        self.extLength = 0
        self.retLength = 0
        self.maxLenReached = False


    def getFeatureDistri(self, lengthsPerFilo):
        self._addToDistributions(lengthsPerFilo)
        return self._getOutput()

    def _addToDistributions(self, lengthsPerFilo)
        listCtr = 0
        for lengths in lengthsPerFilo:
            indivFilos = self._breakIntoFilos(lengths)

            filoCtr = 0
            for filo in indivFilos:
                # continue?
                maxLenTooSmall = self._getMaxLen(filo)
                # continue?
                self._resetValues()

                prev = 0
                for length in filo:
                    self._analyseLength(length)
                    prev = length

                filoCtr += 1
            
            listCtr += 1
    
class InVivoData:
    def __init__(self):
        self.ivDir = os.path.join(self._thisFile, '../../../data/filoLengths/invivo/')
        self.maxLensIV = []
        self.avgExtIV = []
        self.avgRetIV = []
        self.timeAtMaxIV = []

    def getIVData(self):
        return createDict()

    def _thisFile(self):
        pass

    def _pathToFile(self, fileName):
        pass

    def _getData(self, path):
        pass

    def _fillLists(self):
        pass
        
    def _createDict(self):
        pass
