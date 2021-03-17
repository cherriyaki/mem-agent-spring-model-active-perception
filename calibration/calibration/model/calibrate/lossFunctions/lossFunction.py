
from abc import abstractmethod
from calibration import global_
from calibration.model import log
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
        self.run = 1    # The unique number to be assigned to each run output file
        self._setParamIdxes()
        self._setAgent()

    def _setParamIdxes(self):
        idxes = []
        for name in self.params:
            idx = global_.INDEXES[name]
            idxes.append(idx)
        self.idxes = idxes      # The indexes of the varying params

    def _setAgent(self):
        path = os.path.join(global_.getRoot(), "./springAgent")
        self.agent = path

    def runAgent(self, candidate):
        """
        Runs agent with given candidate solution
        """
        cmd = self._getCommand(candidate)
        process = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        # self._checkAgentDone()
        if process.returncode != 0:
            log.w(id=self.id, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), "Failed to run agent"])
            log.w(id=self.id, exc=process.stderr)
            exit(process.stderr)
        else:
            log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"Ran agent successfully. Args={cmd[7:]}"])
            return

    def _getCommand(self, candidate):
        # TEST LOCAL
        # cmd = [f"{self.agent}", f"{self.run}"]
        cmd = ["srun", "--partition=int", "--time=72:00:00", "--nodes=1", "--ntasks=1", "--cpus-per-task=1", f"{self.agent}", f"{self.run}"]
        ctr = 0
        for i in range(1, len(global_.DEFAULTS)):   # for every positional arg after runNum
            if i in self.idxes:     # if this index points to a param we are varying
                if global_.TYPES[i] == "int":
                    cmd.append(f"{int(candidate[ctr])}")
                elif global_.TYPES[i] == "float":
                    cmd.append(f"{global_.truncate(candidate[ctr], 6)}") 
                ctr += 1
            else:       # else, insert the default param in this position
                cmd.append(f"{global_.DEFAULTS[i]}")
        return cmd

    def _checkAgentDone(self):
        # repeatedly check job finish
        pass

    def getOutputContent(self, candidate, **kwargs):
        """
        @param candidate, runOutputDir="dirname"
        """
        dir_ = self._getRunFileDir(**kwargs)
        file = self._getRunFilePath(candidate, dir_)
        if not self._exists(file):
            log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"File {file} does not exist"])
            file = self._findRunNum(dir_)
            log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"Found {file} instead"])
        content = self._getContent(file)
        log.w(id=self.id, line=["DEBUG", global_.fileName(__file__), global_.lineNo(currentframe()), f"Loaded agent output from {file}"])
        self.run += 1   # increment unique number for the next agent run
        return content

    def _getContent(self, file):
        try:
            with open(file, "r") as f:
                content = f.read()
        except:
            tb = traceback.format_exc()
            log.w(id=self.id, line=["ERROR", global_.fileName(__file__), global_.lineNo(currentframe()), f"Failed to open {file}"])
            log.w(id=self.id, exc=tb)
            raise
        return content

    def _getRunFileDir(self, **kwargs):
            root = global_.getRoot()
            if "runOutputDir" in kwargs:
                dir_ = os.path.join(root, kwargs["runOutputDir"])
            else:
                dir_ = root
            return dir_

    def _exists(self, file):
        """
        Checks if file exists 
        """
        if os.path.isfile(file):
            return True
        else: 
            return False

    def _findRunNum(self, dir_):
        """
        Search for file with specific run number instead
        """
        arg = global_.RUNFILE["runNum"]
        for file in os.listdir(dir_):
            if file.endswith(f"{arg}{self.run}_.txt"):
                return os.path.join(dir_, file)

    def _getRunFilePath(self, candidate, dir_):
        """
        Get full runfile path using candidate params
        """
        name = self._getRunFileName(candidate)
        path = os.path.join(dir_, name)
        return path

    def _getRunFileName(self, candidate):
        name = f"{self.analysis}_"
        ext = ".txt"
        ctr = 0
        for k, v in global_.RUNFILE.items():   # for every positional arg in runFile
            i = global_.INDEXES[k]
            name += v   # append the name of this arg
            if k == "runNum":   # when we reach runNum position, append it 
                name += "%i_" % self.run
                continue
            if i in self.idxes:     # if this index points to a param we are varying
                if global_.TYPES[i] == "int":
                    name += "%i_" % candidate[ctr]
                elif global_.TYPES[i] == "float":
                    name += "%g_" % global_.truncate(candidate[ctr], 6)     # the agent runfile name seems to truncate floats without rounding
                ctr += 1
            else:
                if global_.TYPES[i] == "int":
                    name += "%i_" % global_.DEFAULTS[i]
                elif global_.TYPES[i] == "float":
                    name += "%g_" % global_.DEFAULTS[i]
        name += ext
        return name

    @abstractmethod
    def getLosses(self, candidate):
        pass

    

