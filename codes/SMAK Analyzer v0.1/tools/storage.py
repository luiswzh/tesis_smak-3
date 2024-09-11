# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:04:35 2024

@author: luisw
"""

import pandas as pd

import tkinter as tk
from tkinter import filedialog as fd

import pickle

root=tk.Tk()
root.withdraw()

def readfile(title=None):
    return pd.read_pickle(fd.askopenfilename(title=title))

def savefile(df, title=None):
    if isinstance(df, pd.DataFrame):
        df.to_pickle(fd.asksaveasfilename(title=title,defaultextension='.pkl'))
    else:
        with open(fd.asksaveasfilename(title=title,defaultextension='.pkl'), 'wb') as file:
            pickle.dump(df, file)
        
    return

def savefile_xlsx(df, title=None):
    df.to_excel(fd.asksaveasfilename(title=title,defaultextension='.xlsx'))
    return

def save_plots(plot_dict):
    directory=fd.askdirectory()
    for key, value in plot_dict.items():
        value[0].savefig(directory+'/'+key+'.png')
