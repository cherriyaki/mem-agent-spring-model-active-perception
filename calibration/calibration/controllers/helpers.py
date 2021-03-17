import tkinter as tk
from tkinter import ttk

def parse(dict_):
        """ 
        @param Dict {"name": [var1, var2], "name2": var1, name3: listbox}
        Returns copy of dict with empty items removed and text extracted
        """
        d = {}
        for k, v in dict_.items():
            if isinstance(v, list):  # if v is a list
                if not _isEmptyL(v):
                    d[k] = _parseL(v)
            elif isinstance(v, dict):   # if v is a dict
                d[k] = parse(v)
            elif isinstance(v, tk.Listbox):     # if v is a Listbox
                l = _getSelection(v)
                d[k] = _parseL(l)
            else:   # if v is one value
                if _get(v).strip() != "":
                    d[k] = _get(v)
        return d


def _parseL(l):
    list_ = [_get(v) for v in l]
    return list_

def _isEmptyL(l):
    """
    @return True if whole list is empty
    """
    empty = True
    for var in l:   # empty remains true if whole list is empty
        if _get(var).strip() != "":
            empty = False
            break
    return empty

def _get(v):
    """
    Extracts String
    """
    if isinstance(v, tk.StringVar):
        return v.get()
    else:
        return v

def _getSelection(lb):
    """
    @param listbox
    Gets multi selection from listbox
    """
    l = []
    for i in lb.curselection():
        s = lb.get(i)
        l.append(s)
    return l

def clear( inputs):
    """
    @param {"name": [var1, var2], "name2": var1}
    """
    for var in inputs.values():
        if isinstance(var, list):   # var is a list
            clearL(var)
        elif isinstance(var, dict): # var is a dict
            clear(var)
        else:
            _clearV(var)

def _clearV(var):
    if isinstance(var, ttk.Label):    # var is a Label
        var['text'] = ""
    elif isinstance(var, tk.Listbox):   # var is a Listbox
        var.selection_clear(0, 'end')
    else:   # var is one item
        var.set("")

def clearL( vars):
    """
    @param [var1, var2]
    """
    for var in vars:
        _clearV(var)