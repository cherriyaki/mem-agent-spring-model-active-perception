from optimize import Optimizer

class PymooOptimizer(Optimizer):
    def setAnalysis(self, analysis):
        # set analysis
        pass

    def setParams(self, params):
        # convert to lowerB, upperB lists
        pass

    def setObjectives(self, objectives):
        # set list
        pass

    def setLossFn(self, lossFn):
        # set fn variable to the getLossValues()
        pass

    def setAlgo(self, algo):
        # get algo using pymoo factory and algo keyword
        # set fields of algo
        pass

    def optimize(self):
        self._setupProblem()
        self._buildAgent(self.analysis)
        # call minimize()
        # save result
        pass

    def _setupProblem(self):
        # def init
        # def evaluate
    