from input import Input
import lossFunctions
import optimizers

class Calibrator:
    def __init__(self, params, lib, algo, analysis, objectives):
        self.input = Input(params, lib, algo, analysis, objectives)
        self._setup()

    def _setup(self):
        self.lossFn = self._getLossFn(self.input.getAnalysis)
        self.opt = self._getOptimizer(self.input.lib)
        self._configureOpt(self.input.params, self.input.objectives, self.lossFn, self.input.algo)

    def run(self):
        self.opt.optimize()