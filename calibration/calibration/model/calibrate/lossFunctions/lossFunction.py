
from abc import abstractmethod
from calibration import globalFile
from calibration.model import logWriter
import subprocess
import os
from inspect import currentframe

class LossFunction:
    def __init__(self, id_, paramNames):
        """
        @param paramNames: [paramName1, paramName2, ...]
        """
        self.id = id_
        self.params = paramNames
        self._setParamIdxes()
        self._setAgent()

    def _setParamIdxes(self):
        idxes = []
        for name in self.params:
            idx = globalFile.INDEXES[name]
            idxes.append(idx)
        self.idxes = idxes

    def _setAgent(self):
        path = os.path.join(globalFile.getRoot(), "./springAgent")
        self.agent = path

    def _runAgent(self, candidate):
        cmd = self._getCommand(candidate)
        process = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        # self._checkAgentDone()
        if process.returncode != 0:
            logWriter.write(id=self.id, line=["ERROR", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), "Failed to run agent"])
            logWriter.write(id=self.id, exc=process.stderr)
            # test
            # print("agent FAILED")
            exit(process.stderr)
        else:
            # test
            # print("YAY AGENT RAN")
            logWriter.write(id=self.id, line=["DEBUG", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Ran agent successfully. Params={cmd[7:]}"])
            return

    def _getCommand(self, candidate):
        # TEST
        # cmd = [f"{self.agent}"]
        cmd = ["srun", "--partition=int", "--time=72:00:00", "--nodes=1", "--ntasks=1", "--cpus-per-task=1", f"{self.agent}"]
        ctr = 0
        for i in range(len(globalFile.DEFAULTS)):
            if i in self.idxes:     # if this index points to a param we are varying
                cmd.append(f"{candidate[ctr]}")
                ctr += 1
            else:       # else, insert the default param in this position
                cmd.append(f"{globalFile.DEFAULTS[i]}")
        return cmd

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

    

