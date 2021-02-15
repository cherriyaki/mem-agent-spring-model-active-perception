
from .. import config

class LossFunction:
    def __init__(self, analysis):
        self.analysis = analysis

    def _runAgent(self, candidate):
        pass

    def _checkAgentDone(self):
        pass

    def _getOutputContent(self, candidate):
        pass

    @abstractmethod
    def getLosses(self, candidate):
        pass

    

