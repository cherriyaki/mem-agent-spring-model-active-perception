import tkinter as tk
from tkinter import ttk
from calibration.views.homePage import HomePage
from calibration.views.optPage import OptPage
from calibration.views.sensPage import SensPage
from calibration.views.smallPages import ErrPage, MessagePage
from datetime import datetime as dt
import json
from calibration import global_
import os, subprocess
import traceback 
from .helpers import parse, clear, clearL

class App(tk.Tk):
    """
    Main controller class
    """

    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # create and configure container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # create and fill frames dict
        self.frames = {}  
        for F in (HomePage, OptPage, SensPage, MessagePage, ErrPage): #, CampPage
            # create and place frame object
            frame = F(container, self)
            self.frames[F.__name__] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame("HomePage", [])

    def show_frame(self, F, vars):
        """
        Displays the given frame and clears given list of vars
        @param "PageName", [var1, var2]
        """
        frame = self.frames[F]
        frame.tkraise()
        clearL(vars)

    def runOpt(self, inputs):
        """
        Run optimization
        @param {"name": [var1, var2], "name2": var1}
        """
        self._run(inputs, "opt")

    def runSens(self, inputs):
        """
        Run sensitivity analysis 
        @param {"name": [var1, var2], "name2": var1}
        """
        self._run(inputs, "sens")

    def _run(self, inputs, job):
        id_ = self._createID(job)
        dict_ = parse(inputs)
        str_ = self._dictToJson(dict_)
        print(str_)
        json = self._jsonFileName(id_)
        written = self._writeFile(json, str_)
        if not written:
            return
        clear(inputs)
        ran = self._runOnCamp(id_, dict_)
        if not ran:
            return
        self._showNext(id_)

    def _showNext(self, id_):
        page = "MessagePage"
        frame = self.frames[page]
        log = self._logFileName(id_)
        res = self._resFileName(id_)
        frame.show(f"Session ID = {id_}\n Please remember session ID for locating files and CAMP job tracking\n File locations:\nJson input file: {json}\n Log: {log}\n Result file: {res}")
        frame.tkraise()

    def _dictToJson(self, dict_):
        """
        Add date item and convert dict to string
        """
        dtObj = dt.now()
        time = f"{dtObj.year}-{dtObj.month}-{dtObj.day} {dtObj.hour}:{dtObj.minute}:{dtObj.second}"
        dict_["Time"] = time
        str_ = json.dumps(dict_)
        return str_

    def _jsonFileName(self, id_):
        """
        Gets json file name with given type and id
        """
        root = global_.getRoot() 
        f = os.path.join(root, f"calibration/data/inputHistory/{id_}.json")
        return f

    def _logFileName(self, id_):
        root = global_.getRoot() 
        f = os.path.join(root, f"calibration/logs/{id_}.log")
        return f

    def _resFileName(self, id_):
        root = global_.getRoot() 
        if "sens" in id_:
            f = os.path.join(root, f"calibration/output/results/{id_}.csv")
        else:
            f = os.path.join(root, f"calibration/output/results/{id_}.res")
        return f

    def _writeFile(self, file, str_):
        try:
            with open(file, "w") as f:
                f.write(str_)
            return True
        except:
            tb = traceback.format_exc()
            self._showErr(f"Failed to open {file}. \n {tb}")
            return False

    def _runOnCamp(self, id_, dict_):
        analysis = dict_['analysis']
        email = dict_['email']
        user = dict_['user']
        cmd = [self._campScript(), "--analysis", f"{analysis}", "--email", f"{email}", "--user", f"{user}", "--id", f"{id_}"]
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if process.returncode != 0:
            self._showErr(f"Failed to run campScript.sh\n {process.stderr}")
            return False
        else:
            return True
        
    def _campScript(self):
        root = global_.getRoot()
        file = os.path.join(root, "calibration/calibration/model/./campScript.sh")
        return file
    
    def _getCampScript(self):
        root = global_.getRoot()
        file = os.path.join(root, "calibration/calibration/model/./getCampData.sh")
        return file

    def _showErr(self, err):        
        frame = self.frames["ErrPage"]
        frame.show(err)
        frame.tkraise()

    def _createID(self, job):
        dtObj = dt.now()
        id_ = f"{dtObj.year}{dtObj.month}{dtObj.day}{dtObj.hour}{dtObj.minute}{dtObj.second}"
        id_ = f"{job}_{id_}"
        return id_
    
    

