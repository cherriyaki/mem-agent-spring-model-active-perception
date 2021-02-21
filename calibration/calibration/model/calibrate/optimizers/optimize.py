class Optimizer:
    @abstractmethods
    def setParams(self, params):
        pass

    def setObjectives(self, objectives):
        pass

    def setLossFn(self, lossFn):
        pass

    def setAlgo(self, algo):
        pass

    def optimize(self):
        pass

    
