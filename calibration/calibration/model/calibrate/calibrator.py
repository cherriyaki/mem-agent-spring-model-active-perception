from input import Input
import lossFunctions
import optimizers

class Calibrator:
    def __init__(self, id):
        # with id as arg
        self.input = Input()
        self._setInput(id)
        self._setup()

    def run(self):
        self.opt.optimize()

    def _setInput(self, id):
        # init jsonconverter
        # get data as a dict
        # set Input fields
        pass

    def _setup(self):
        self.lossFn = self._getLossFn(self.input.getAnalysis)
        self.opt = self._getOptimizer(self.input.lib)
        self._configureOpt()

    def _getLossFn(self, analysis):
        # check analysis type
        # return the corresponding lossfn class
        pass

    def _getOptimizer(self, lib):
        # init opt class with lib name
        #  return
        pass

    def _configureOpt(self):
        # set self.input.params, self.input.objectives, self.lossFn, self.input.algo
        pass

    