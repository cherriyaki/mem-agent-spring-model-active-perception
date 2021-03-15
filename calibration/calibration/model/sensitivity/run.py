import json 
from calibration import global_
from calibration.model import log
from inspect import currentframe
import traceback
from calibration.model.calibrate.lossFunctions.filoLengthsLoss import FiloLengthsLoss
import os

class SensRunner:
    def __init__(self, id_):
        self.id = id_
        self.job = "sens"
        self.out = ""

    def run(self):
        log.w(id=self.id, job=self.job, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), "Started sensitivity experiment"])
        self.input = self._getInputFromJson()
        self._setup()
        self._testEachParam()
        self._writeOut()

    def _getInputFromJson(self):
        file = self._getJsonFile()
        try:
            with open(file) as f: 
                data = json.load(f) 
        except:
            tb = traceback.format_exc()
            log.w(id=self.id, job=self.job, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), f"Failed to open or load {file}"])
            log.w(id=self.id, job=self.job, exc=tb)
            raise       # Throw the caught exception
        log.w(id=self.id, job=self.job, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), "JSON input loaded"])
        return data

    def _getJsonFile(self):
        root = global_.getRoot()
        file = os.path.join(root, f"calibration/data/inputHistory/{self.job}_{self.id}.json")
        return file

    def _setup(self):
        self._setLossFn(self.input["analysis"])
        self.params = self.input["params"].keys()
        self._setupOut()

    def _setLossFn(self, analysis):
        self.lossFn = FiloLengthsLoss(self.id, list(self.input["params"].keys()))      # Default
        # Add code here to set a different loss function based on argument `analysis`
        log.w(id=self.id, job=self.job, line=["INFO", global_.fileName(__file__), global_.lineNo(currentframe()), f"Set loss function as {type(self.lossFn).__name__}"])

    def _setupOut(self):
        for p in self.params:
            self.out += f"{p},"
        self.out += ","
        for o in global_.OBJ:
            self.out += f"{o},"

    def _testEachParam(self):
        for p in self.params:
            vals = self._getVals(p)
            others = self.params - [p]
            defs = self._getDefaults(others)
            for v in vals:
                candidate = []
                for q in self.params:   # build candidate in order
                    if q == p:  # varied param
                        candidate.append(v)
                    else:   # default param
                        candidate.append(defs[q])
                losses = self.lossFn.getLosses(candidate).values()
                self._addToOut(candidate, losses)

    def _addToOut(self, cand, losses):
        self.out += "\n"
        for c in cand:
            self.out += f"{c},"
        self.out += ","
        for l in losses:
            self.out += f"{l},"

    def _getDefaults(self, params):
        """
        @param [p1, p2]
        @return {"p1": def, "p2": def}
        """
        defaults = {}
        # defaults = []
        for p in params:
            i = global_.INDEXES[p]
            defaults[p] = global_.DEFAULTS[i]
            # defaults.append(global_.DEFAULTS[i])
        return defaults

    def _getVals(self, p):
        """
        For given param, get the list of vals to test
        """
        start, end, step = self.input["params"][p]
        vals = []
        v = start
        while v <= end:
            vals.append(v)
            v += step
        return vals

    def _writeOut(self):
        file = self._outFile()
        try:
            with open(file, "w") as f:
                f.write(self.out)
        except:
            tb = traceback.format_exc()
            log.w(id=self.id, job=self.job, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), f"Failed to open or load {file}"])
            log.w(id=self.id, job=self.job, exc=tb)
            raise       # Throw the caught exception

    def _outFile(self):
        root = global_.getRoot()
        file = os.path.join(root, f"calibration/output/results/{self.job}_{self.id}.csv")
        return file