# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:55:35 2024

@author: luisw
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle
import pandas as pd

def log_downsample(x, y, N):
    log_range=np.logspace(np.log10(x[0]+1e-6), np.log10(x[-1]),N+1)
    
    x_new=[(log_range[i+1]+log_range[i])/2 for i in range(N)]
    
    y_new=[]
    
    df=pd.DataFrame()
    df['x']=x
    df['y']=y
    
    for i in range(N):
        bucket=np.log(df.y[df.x.between(log_range[i],log_range[i+1])])
        y_new.append(np.exp(bucket.mean()))
    
    return x_new, np.array(y_new)

def power_slope(slope,x,y):
    plaw_x=np.logspace(-2, np.log10(2.5))
    plaw_y=plaw_x**(slope)
    offset=np.log(plaw_y[-1])-np.log(y[-1]*x[-1])
    plaw_y_o=np.exp(np.log(plaw_y)-offset)
    
    return plaw_x, plaw_y_o


def compute(df, title):
    data=df[df['valid_wind']]
    x=data.apply(lambda x: x['timestamp_e'].total_seconds(), axis=1)
    y=data['WIND_true_magnitude']
    
    low_freq=1/(x.iloc[-1]-x.iloc[0])
    freq=np.linspace(low_freq,2.5,len(x))
    freq_ang=freq*2*np.pi
    
    spectra=lombscargle(x, y, freq_ang, precenter=True, normalize=True)
    
    fig,ax=plt.subplots()
    
    SF=spectra*freq
    
    ax.plot(freq,SF, color='0.8')
    ax.plot(*log_downsample(freq, SF, len(x)//20))
    ax.plot(*power_slope(-2/3,*log_downsample(freq, SF, len(x)//20)),label='-2/3 slope')
    
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude * Frequency')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    
    fig.suptitle(title, y=0.95)
    
    return fig, ax, freq, spectra