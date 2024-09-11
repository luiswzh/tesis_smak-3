# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:26:48 2024

@author: luisw

SLERJ Datalogger parser

INPUT:
    SLERJ DATALOG
    
OUTPUT:
    Pandas dataframe file and pickle
"""

import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd

root=tk.Tk()
root.withdraw()

fpath=fd.askopenfilename()

df=pd.read_csv(fpath, delimiter=' ', header=None)
#df=pd.read_fwf(fpath, header=None)

tag_list = [[df[column].iloc[0], column+1] for column in df if isinstance(df[column].iloc[0],str)]

newdf=pd.DataFrame()

newdf['timestamp']=pd.to_datetime(df[0].astype(str),format="%y%m%d%H%M%S.%f")

for tag in tag_list:
    newdf[tag[0]]=df[tag[1]]

newdf.to_pickle(fd.asksaveasfilename(defaultextension='.pkl'))
