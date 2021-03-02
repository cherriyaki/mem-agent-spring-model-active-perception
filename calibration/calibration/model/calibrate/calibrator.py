import os, sys
import json 
from calibration import global_
from .lossFunctions.filoLengthsLoss import FiloLengthsLoss
from .optimizers.pymooOpt import PymooOptimizer
from calibration.model import log
from inspect import currentframe
import traceback

class Calibrator:
    def __init__(self, id_):
        self.id = id_

    def run(self):
        log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), "Calibrator started running"])
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
            log.w(id=self.id, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), f"Failed to open or load {file}"])
            log.w(id=self.id, exc=tb)
            raise       # Throw the caught exception
        log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), "JSON input loaded"])
        return data

    def _getJsonFile(self):
        root = global_.getRoot()
        file = os.path.join(root, f"calibration/data/inputHistory/input_{self.id}.json")
        return file

    def _setup(self):
        self._setLossFn(self.input["analysis"])
        self._setOptimizer(self.input["lib"])
        self._configureOpt()

    def _setLossFn(self, analysis):
        self.lossFn = FiloLengthsLoss(self.id, list(self.input["params"].keys()))      # Default
        # Add code here to set a different loss function based on argument `analysis`
        log.w(id=self.id, line=["INFO", global_.fileName(__file__), global_.lineNo(currentframe()), f"Set loss function as {type(self.lossFn).__name__}"])

    def _setOptimizer(self, lib):
        self.opt = PymooOptimizer(self.id)     # Default
        # Add code here to set a differentt optimizer library based on argument `lib`
        log.w(id=self.id, line=["INFO", global_.fileName(__file__), global_.lineNo(currentframe()), f"Set optimizer lib as {type(self.opt).__name__}"])

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