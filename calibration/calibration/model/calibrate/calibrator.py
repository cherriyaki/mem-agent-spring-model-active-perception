import os, sys
import json 
from calibration import globalFile
from .lossFunctions.filoLengthsLoss import FiloLengthsLoss
from .optimizers.pymooOpt import PymooOptimizer
from calibration.model import logWriter
from inspect import currentframe
import traceback

class Calibrator:
    def __init__(self, id_):
        self.id = id_

    def run(self):
        self.input = self._getInputFromJson()
        self._setup()
        self.opt.optimize()

    def _getInputFromJson(self):
        file = self._getJsonFile()
        try:
            with open(file) as f: 
                data = json.load(f) 
        except:
            tb = traceback.format_exc()
            logWriter.write(id=self.id, line=["ERROR", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Failed to open or load {file}"])
            logWriter.write(id=self.id, exc=tb)
            raise       # Throw the caught exception
        logWriter.write(id=self.id, line=["DEBUG", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), "JSON input loaded"])
        return data

    def _getJsonFile(self):
        root = globalFile.getRoot()
        file = os.path.join(root, f"calibration/data/inputHistory/input_{self.id}.json")
        return file

    def _setup(self):
        self._setLossFn(self.input["analysis"])
        self._setOptimizer(self.input["lib"])
        self._configureOpt()

    def _setLossFn(self, analysis):
        self.lossFn = FiloLengthsLoss(self.id)      # Default
        # Add code here to set a different loss function based on argument `analysis`
        logWriter.write(id=self.id, line=["INFO", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Set loss function as {type(self.lossFn).__name__}"])

    def _setOptimizer(self, lib):
        self.opt = PymooOptimizer(self.id)     # Default
        # Add code here to set a differentt optimizer library based on argument `lib`
        logWriter.write(id=self.id, line=["INFO", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Set optimizer lib as {type(self.opt).__name__}"])

    def _configureOpt(self):
        self.opt.setParams(self.input["params"])
        self.opt.setObjectives(self.input["objectives"])
        self.opt.setLossFn(self.lossFn)
        self.opt.setAlgo(self.input["algorithm"])

    # @staticmethod
    # def _lineNo():
    #     return getframeinfo(currentframe()).lineno

# if __name__ == '__main__':
#     cal = Calibrator(sys.argv[1])
#     cal.run()