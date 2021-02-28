
from abc import abstractmethod
from calibration import globalFile
from calibration.model import logWriter
import subprocess
import os
from inspect import currentframe
import traceback

class LossFunction:
    def __init__(self, id_, paramNames, analysis):
        """
        @param paramNames: [paramName1, paramName2, ...]
        """
        self.id = id_
        self.params = paramNames
        self.analysis = analysis
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

    def runAgent(self, candidate):
        """
        Runs agent with given candidate solution
        """
        cmd = self._getCommand(candidate)
        process = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        # self._checkAgentDone()
        if process.returncode != 0:
            logWriter.write(id=self.id, line=["ERROR", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), "Failed to run agent"])
            logWriter.write(id=self.id, exc=process.stderr)
            exit(process.stderr)
        else:
            logWriter.write(id=self.id, line=["DEBUG", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Ran agent successfully. Args={cmd[7:]}"])
            return

    def _getCommand(self, candidate):
        # TEST LOCAL
        cmd = [f"{self.agent}"]
        # cmd = ["srun", "--partition=int", "--time=72:00:00", "--nodes=1", "--ntasks=1", "--cpus-per-task=1", f"{self.agent}"]
        ctr = 0
        for i in range(len(globalFile.DEFAULTS)):   # for every positional arg
            if i in self.idxes:     # if this index points to a param we are varying
                if globalFile.TYPES[i] == "int":
                    cmd.append(f"{int(candidate[ctr])}")
                elif globalFile.TYPES[i] == "float":
                    cmd.append(f"{candidate[ctr]}") # :.1f
                ctr += 1
            else:       # else, insert the default param in this position
                cmd.append(f"{globalFile.DEFAULTS[i]}")
        return cmd

    def _checkAgentDone(self):
        # repeatedly check job finish
        pass

    def getOutputContent(self, candidate, **kwargs):
        """
        @param candidate, runOutputDir="dirname"
        """
        file = self._getRunFilePath(candidate, **kwargs)
        try:
            with open(file, "r") as f:
                content = f.read()
        except:
            tb = traceback.format_exc()
            logWriter.write(id=self.id, line=["ERROR", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Failed to open {file}"])
            logWriter.write(id=self.id, exc=tb)
            raise
        logWriter.write(id=self.id, line=["DEBUG", globalFile.fileName(__file__), globalFile.lineNo(currentframe()), f"Loaded agent output from {file}"])
        return content

    def _getRunFilePath(self, candidate, **kwargs):
        name = self._getRunFileName(candidate)
        root = globalFile.getRoot()
        if "runOutputDir" in kwargs:
            path = os.path.join(root, kwargs["runOutputDir"], name)
        else:
            path = os.path.join(root, name)
        return path

    def _getRunFileName(self, candidate):
        name = f"{self.analysis}_"
        ext = ".txt"
        ctr = 0
        for k, v in globalFile.RUNFILE.items():   # for every positional arg in runFile
            i = globalFile.INDEXES[k]
            name += v
            if i in self.idxes:     # if this index points to a param we are varying
                if globalFile.TYPES[i] == "int":
                    name += "%i_" % candidate[ctr]
                elif globalFile.TYPES[i] == "float":
                    name += "%g_" % candidate[ctr]
                ctr += 1
            else:
                if globalFile.TYPES[i] == "int":
                    name += "%i_" % globalFile.DEFAULTS[i]
                elif globalFile.TYPES[i] == "float":
                    name += "%g_" % globalFile.DEFAULTS[i]
        name += ext
        return name

    @abstractmethod
    def getLosses(self, candidate):
        pass

    

