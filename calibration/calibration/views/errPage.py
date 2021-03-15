from .viewsGlobal_ import LARGEFONT
import tkinter as tk
from tkinter import ttk

class ErrPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.allVars = []
        tk.Frame.__init__(self, parent)
        self._addTop()

    def _addTop(self):
        topFrame = tk.Frame(self)
        topFrame.pack(fill = tk.X)
        # Create and place title label
        label = ttk.Label(topFrame, text ="Oh no :(", font = LARGEFONT)
        label.grid(row = 0, column = 4, columnspan = 4) #, padx = 10, pady = 10
        # Create and place button
        homeBtn = ttk.Button(topFrame, text ="Home",
                            command = lambda : self.controller.show_frame("HomePage", self.allVars))
        homeBtn.grid(row = 0, column = 0)

    def show(self, message):
        frame = tk.Frame(self)
        frame.pack(fill = tk.X)
        lbl = ttk.Label(frame, text = message, font = "Calibri, 11, bold")
        lbl.pack()
        self.allVars.append(lbl)