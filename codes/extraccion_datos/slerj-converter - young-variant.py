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

df=pd.read_csv(fpath, header=None, delim_whitespace=True)

newdf=pd.DataFrame()

newdf['timestamp']=pd.to_datetime(df[0].astype(str),format="%y%m%d%H%M%S.%f")

newdf['u']=df[1]
newdf['v']=df[2]
newdf['w']=df[3]
newdf['T']=df[4]

save_dir=fd.askdirectory()
filename = input("Output file name: ")
#newdf.to_pickle(save_dir+"/"+filename+".pkl")
