class Input:
    def __init__(self,
                params={"filvary": [0.1,4], "filspacing": [1,3], "actinmax": [500, 600]},
                lib="pymoo",
                algorithm="NSGA2",
                analysis="filo_lengths",
                objectives=["maxLen", "averageExtendingTime"]
    ):
        self.params = params
        self.lib = lib
        self.algorithm = algorithm
        self.analysis = analysis
        self.objectives = objectives

    def getParams(self):
        return self.params

    def getLib(self):
        return self.lib

    def getAlgo(self):
        return self.algorithm

    def getAnalysis(self):
        return self.analysis

    def getObjectives(self):
        return self.objectives
