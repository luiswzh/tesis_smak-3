# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:28:19 2024

@author: luisw

Rosa de los vientos smak-3
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib
import pandas as pd
import windrose


def windir(direction):
    if direction<0:
        direction=direction+360
    return direction


matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 5,
})

"""
Lectura de datos
"""

data=pd.read_pickle('smak_data.pkl')

"""
Graficado
"""

fig, axes=plt.subplots(2,3, subplot_kw={'projection': 'windrose'})

i=0
for ax in axes.flatten():
    ax.bar(data[i].apply(lambda x: windir(x['wind_dir']),axis=1), data[i].WIND_true_magnitude, normed=True, bins=[0,5,10,15], colors=('lightgrey','darkgrey','dimgrey','black')) 
    i+=1
    ax.set_title('F0'+str(i), loc='left')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))

axes[1,2].legend(loc='lower right', decimal_places=0).set_title('Viento [m/s]')
fig.suptitle('Rosa de los vientos SMAK-3', size=10)

fig.set_size_inches(w=6, h=5)

fig.savefig('wr_smak.pdf')
