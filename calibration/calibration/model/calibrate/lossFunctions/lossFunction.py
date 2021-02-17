
from .. import config

class LossFunction:
    def __init__(self, analysis):
        self.analysis = analysis

    def _runAgent(self, candidate):
        # try: run agent with candidate args
        self._checkAgentDone()
        # if finish, return
        pass

    def _checkAgentDone(self):
        # repeatedly check job finish
        pass

    def _getOutputContent(self, candidate):
        # get file from agent run
        # if empty, bubble error
        pass

    @abstractmethod
    def getLosses(self, candidate):
        pass

    

