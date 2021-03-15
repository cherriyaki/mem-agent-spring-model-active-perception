from .viewsGlobal_ import LARGEFONT
import tkinter as tk
from tkinter import ttk

# pg1 calibration

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
        tk.Frame.__init__(self, parent)
        self._addTop()
        self._addParamFields()
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

    def _addParamFields(self):
        paramsFrame = tk.Frame(self)
        paramsFrame.pack(fill = tk.BOTH)
        #-- epsilon
        epsilonLbl = ttk.Label(paramsFrame, text = "Epsilon:", font = ("Calibri", 10, "bold"))     # param label
        epsilonLbl.grid(row = 1, column = 0)
        low1 = ttk.Label(paramsFrame, text = "lower", font = ("Calibri", 8))   # lower label
        low1.grid(row = 1, column = 1)
        epsilonL = tk.Entry(paramsFrame, width = 5)   # lower input field
        epsilonL.grid(row = 1, column = 2)
        up1 = ttk.Label(paramsFrame, text = "upper", font = ("Calibri", 8))    # upper label
        up1.grid(row = 1, column = 3)
        epsilonU = tk.Entry(paramsFrame, width = 5)   # upper input field
        epsilonU.grid(row = 1, column = 4)


    def _addBottom(self):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(fill = tk.X)
        # Create and place button
        optBtn = ttk.Button(bottomFrame, text ="Optimize",
                            command = lambda : controller.show_frame(Page2, []))
        optBtn.grid(row = 10, column = 4, padx = 10, pady = 10)
