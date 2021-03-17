from .viewsGlobal_ import LARGEFONT
import tkinter as tk
from tkinter import ttk

# pg1 calibration

from calibration import global_

# input
# email for optimize finish/error
# username for camp login
# params, lib, algo, obj, analysis
# optimize button

# next screen
# some kinda session id - slurm id, timestamp?
class OptPage(tk.Frame):
     
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.inputs = {}
        tk.Frame.__init__(self, parent)
        self._addTop()
        self._addMisc()
        self._addParams()
        self._addBottom()
        

    def _addTop(self):
        topFrame = tk.Frame(self)
        topFrame.pack(fill = tk.X)
        # Create and place title label
        label = ttk.Label(topFrame, text ="Parameter Optimization", font = LARGEFONT)
        label.grid(row = 0, column = 4, columnspan = 4) #, padx = 10, pady = 10
  
        # Create and place button
        homeBtn = ttk.Button(topFrame, text ="Home",
                            command = lambda : self.controller.show_frame("HomePage", []))
        homeBtn.grid(row = 0, column = 0)

    def _addMisc(self):
        frame = tk.Frame(self)
        frame.pack(fill = tk.X)
        self._addOneValueField(frame, "user", 0, 0, False)
        self._addOneValueField(frame, "email", 0, 3, False)
        self._addDropdown(frame, "analysis", global_.ANALYSIS, 0, 6)
        self._addDropdown(frame, "algorithm", global_.ALGOS, 0, 9)
        self._addMultiSelect("objectives", global_.OBJ)

    def _addParams(self):
        frame = tk.Frame(self)
        frame.pack(fill = tk.X)
        self.inputs["params"] = {}
        self._addFullField(frame, "epsilon", 1, 0)
        self._addFullField(frame, "VconcST", 1, 5)
        self._addOneValueField(frame, "gradientType", 1, 10, True)
        self._addFullField(frame, "filVary", 2, 0)
        self._addFullField(frame, "filTipMax", 2, 5)
        self._addFullField(frame, "tokenStrength", 2, 10)
        self._addFullField(frame, "filSpacing", 3, 0)
        self._addFullField(frame, "actinMax", 3, 5)
        self._addFullField(frame, "filSpringC", 3, 10)
        self._addFullField(frame, "filSpringL", 4, 0)

    def _addFullField(self, parent, name, r, start):
        lbl = ttk.Label(parent, text = f"{name}", font = ("Calibri", 10, "bold"))     # param label
        lbl.grid(row = r, column = start)
        start +=1
        LL = ttk.Label(parent, text = "lower bound", font = ("Calibri", 8))   # lower label
        LL.grid(row = r, column = start)
        start +=1
        low = tk.StringVar()
        LE = tk.Entry(parent, width = 4, textvariable = low)   # lower input field
        LE.grid(row = r, column = start)
        start +=1
        UL = ttk.Label(parent, text = "upper bound", font = ("Calibri", 8))    # upper label
        UL.grid(row = r, column = start)
        start +=1
        up = tk.StringVar()
        UE = tk.Entry(parent, width = 4, textvariable = up)   # upper input field
        UE.grid(row = r, column = start)
        start +=1
        self.inputs["params"][name] = [low, up]

    def _addOneValueField(self, parent, name, r, start, param):
        lbl = ttk.Label(parent, text = f"{name}", font = ("Calibri", 10, "bold"))     # param label
        lbl.grid(row = r, column = start)
        start +=1
        value = tk.StringVar()
        LE = tk.Entry(parent, width = 4, textvariable = value)   # input field
        LE.grid(row = r, column = start)
        if param:
            self.inputs["params"][name] = value
        else:
            self.inputs[name] = value

    def _addDropdown(self, parent, name, list_, r, start):
        var = tk.StringVar()
        var.set(list_[0])    # default value
        lbl = ttk.Label(parent, text = f"{name}", font = ("Calibri", 10, "bold"))     # label
        lbl.grid(row = r, column = start)
        start +=1
        w = tk.OptionMenu(parent, var, *list_)     # dropdown
        w.grid(row = r, column = start)
        self.inputs[name] = var

    def _addMultiSelect(self, name, list_):
        frame = tk.Frame(self)
        frame.pack(fill = tk.Y)
        lbl = ttk.Label(frame, text = f"{name}", font = ("Calibri", 10, "bold"))     # label
        lbl.pack(fill=tk.Y)
        lb = tk.Listbox(frame, selectmode = "multiple")    # ListBox
        lb.pack(fill = tk.BOTH)
        for e in list_:
            lb.insert(tk.END, e)
        self.inputs[name] = lb

    def _addBottom(self):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(fill = tk.X)
        # Create and place button
        optBtn = ttk.Button(bottomFrame, text ="Optimize",
                            command = lambda : self.controller.runOpt(self.inputs))
        optBtn.grid(row = 10, column = 4, padx = 10, pady = 10)
