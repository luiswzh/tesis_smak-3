# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:45:49 2024

@author: luisw

Rosa de los vientos young 81000
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

data=pd.read_pickle('young_data.pkl')

"""
Graficado
"""

fig, axes=plt.subplots(2,3, subplot_kw={'projection': 'windrose'})

i=0
for ax in axes.flatten():
    ax.bar(data[i].apply(lambda x: windir(x['dir']),axis=1), data[i].wind, normed=True, bins=[0,2,4,6], colors=('lightgrey','darkgrey','dimgrey','black')) 
    i+=1
    ax.set_title('F0'+str(i), loc='left')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))

axes[1,2].legend(loc='lower right', decimal_places=0).set_title('Viento [m/s]')
fig.suptitle('Rosa de los vientos YOUNG 81000', size=10)

fig.set_size_inches(w=6, h=5)

fig.savefig('wr_young.pdf')
