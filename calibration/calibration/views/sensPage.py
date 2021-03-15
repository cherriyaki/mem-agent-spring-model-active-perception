from .viewsGlobal_ import LARGEFONT
from calibration import global_
import tkinter as tk
from tkinter import ttk

class SensPage(tk.Frame):
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
        label = ttk.Label(topFrame, text ="Sensitivity Test", font = LARGEFONT)
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

    def _addParams(self):
        frame = tk.Frame(self)
        frame.pack(fill = tk.X)
        self.inputs["params"] = {}
        self._addFullField(frame, "epsilon", 1, 0)
        self._addFullField(frame, "VconcST", 1, 7)
        self._addOneValueField(frame, "gradientType", 1, 14, True)
        self._addFullField(frame, "filVary", 2, 0)
        self._addFullField(frame, "filTipMax", 2, 7)
        self._addFullField(frame, "tokenStrength", 2, 14)
        self._addFullField(frame, "filSpacing", 3, 0)
        self._addFullField(frame, "actinMax", 3, 7)
        self._addFullField(frame, "filSpringC", 3, 14)
        self._addFullField(frame, "filSpringL", 4, 0)

    def _addFullField(self, parent, name, r, start):
        lbl = ttk.Label(parent, text = f"{name}", font = ("Calibri", 10, "bold"))     # param label
        lbl.grid(row = r, column = start)
        start +=1
        LL = ttk.Label(parent, text = "start value", font = ("Calibri", 8))   # lower label
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
        SL = ttk.Label(parent, text = "step", font = ("Calibri", 8))    # step label
        SL.grid(row = r, column = start)
        start +=1
        step = tk.StringVar()
        SE = tk.Entry(parent, width = 4, textvariable = step)     # step input field
        SE.grid(row = r, column = start)
        self.inputs["params"][name] = [low, up, step]


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

    def _addBottom(self):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(fill = tk.X)
        # Create and place button
        optBtn = ttk.Button(bottomFrame, text ="Run",
                            command = lambda : self.controller.runSens(self.inputs))
        optBtn.grid(row = 10, column = 4, padx = 10, pady = 10)
        # clear btn
        clearBtn = ttk.Button(bottomFrame, text = "Clear", 
                            command = lambda : self.controller.clear(self.inputs))
        clearBtn.grid(row = 10, column = 7)

class SensNextPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.allVars = []
        tk.Frame.__init__(self, parent)
        self._addTop()

    def _addTop(self):
        topFrame = tk.Frame(self)
        topFrame.pack(fill = tk.X)
        # Create and place button
        homeBtn = ttk.Button(topFrame, text ="Home",
                            command = lambda : self.controller.show_frame("HomePage", self.allVars))
        homeBtn.grid(row = 0, column = 0)

    def show(self, message):
        frame = tk.Frame(self)
        frame.pack(fill = tk.X)
        lbl = ttk.Label(frame, text = message, font = "Calibri, 14")
        lbl.pack()
        self.allVars.append(lbl)
