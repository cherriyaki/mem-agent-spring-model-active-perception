import tkinter as tk
from tkinter import ttk
from calibration.views.homePage import HomePage
from calibration.views.optPage import OptPage
from calibration.views.sensPage import SensPage, SensNextPage
from calibration.views.errPage import ErrPage
from datetime import datetime as dt
import json
from calibration import global_
import os
import traceback 

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
        for F in (HomePage, OptPage, SensPage, SensNextPage, ErrPage): #, CampPage
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
        self._clearVars(vars)

    def runSens(self, inputs):
        """
        Run sensitivity analysis 
        @param {"name": [var1, var2], "name2": var1}
        """
        id_ = self._createID()
        dict_ = self._parseDict(inputs)
        str_ = self._dictToJson(dict_)
        json = self._jsonFileName(id_, "sens")
        self.clear(inputs)
        written = self._writeFile(json, str_)
        if not written:
            return
        # backend code
        self._showSensNext()
        
    def _showSensNext(self):
        frame = self.frames["SensNextPage"]
        log = self._logFileName(id_, "sens")
        res = self._resFileName(id_, "sens")
        frame.show(f"Session ID = {id_}\n Please remember session ID for locating files and CAMP job tracking\n File locations:\nJson input file: {json}\n Log: {log}\n Result file: {res}")
        frame.tkraise()

    def _parseDict(self, dict_):
        """
        @param {"name": [var1, var2], "name2": var1}
        Returns copy of dict with empty items removed and text extracted
        """
        d = {}
        for k, v in dict_.items():
            if isinstance(v, list):  # if v is a list
                empty = True
                for var in v:   # empty remains true if whole list is empty
                    if var.get().strip() != "":
                        empty = False
                        break
                if not empty:
                    d[k] = [var.get() for var in v]
            elif isinstance(v, dict):   # if v is a dict
                d[k] = self._parseDict(v)
            else:   # if v is one value
                if v.get().strip() != "":
                    d[k] = v.get()
        return d

    def _dictToJson(self, dict_):
        """
        Add date item and convert dict to string
        """
        dtObj = dt.now()
        time = f"{dtObj.year}-{dtObj.month}-{dtObj.day} {dtObj.hour}:{dtObj.minute}:{dtObj.second}"
        dict_["Time"] = time
        str_ = json.dumps(dict_)
        return str_

    def _jsonFileName(self, id_, name):
        """
        Gets json file name with given type and id
        """
        root = global_.getRoot() 
        f = os.path.join(root, f"calibration/data/inputHistory/{name}_{id_}.json")
        return f

    def _logFileName(self, id_, name):
        root = global_.getRoot() 
        f = os.path.join(root, f"calibration/logs/{name}_{id_}.log")
        return f

    def _resFileName(self, id_, name):
        root = global_.getRoot() 
        f = os.path.join(root, f"calibration/output/results/{name}_{id_}.csv")
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

    def _showErr(self, err):        
        frame = self.frames["ErrPage"]
        frame.show(err)
        frame.tkraise()

    def _createID(self):
        dtObj = dt.now()
        id_ = f"{dtObj.year}{dtObj.month}{dtObj.day}{dtObj.hour}{dtObj.minute}{dtObj.second}"
        return id_
    
    def clear(self, inputs):
        """
        @param {"name": [var1, var2], "name2": var1}
        """
        for var in inputs.values():
            if isinstance(var, list):   # var is a list
                self._clearVars(var)
            elif isinstance(var, dict): # var is a dict
                self.clear(var)
            elif isinstance(var, ttk.Label):
                var['text'] = ""
            else:   # var is one item
                var.set("")

    def _clearVars(self, vars):
        """
        @param [var1, var2]
        """
        for var in vars:
            if isinstance(var, ttk.Label):
                var['text'] = ""
            else:
                var.set("")

