from .viewsGlobal_ import LARGEFONT
import tkinter as tk
from tkinter import ttk
from .optPage import OptPage
from .sensPage import SensPage

class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
         
        # Create and place title label
        label = ttk.Label(self, text ="Home", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
  
        # Create and place button
        optPgBtn = ttk.Button(self, text ="Optimize Params",
        command = lambda : controller.show_frame("OptPage", []))
        optPgBtn.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # Create and place button
        sensPgBtn = ttk.Button(self, text ="Sensitivity Test",
        command = lambda : controller.show_frame("SensPage", []))
        sensPgBtn.grid(row = 2, column = 1, padx = 10, pady = 10)

        # # Create and place button
        # cmpPgBtn = ttk.Button(self, text ="Retrieve from CAMP",
        # command = lambda : controller.show_frame(CampPage, []))
        # cmpPgBtn.grid(row = 3, column = 1, padx = 10, pady = 10)


# pg3 get session data from camp