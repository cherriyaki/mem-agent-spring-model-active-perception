from abc import abstractmethod

class Optimizer:
    def __init__(self, id_):
        self.id = id_
        self.fn = None

    @abstractmethod
    def setParams(self, params):
        pass
    
    @abstractmethod
    def setObjectives(self, objectives):
        pass

    @abstractmethod
    def setLossFn(self, lossFn):
        pass

    @abstractmethod
    def setAlgo(self, algo):
        pass

    @abstractmethod
    def optimize(self):
        pass

    
