# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:01:28 2024

@author: luisw

Rosa de los vientos SMAK-3, puente
"""

import matplotlib.pyplot as plt
import matplotlib
import windrose as wr
import matplotlib.ticker as mtick
import pandas as pd

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

def windir(direction):
    if direction<0:
        direction=direction+360
    return direction

"""
Lectura de datos
"""
data=pd.read_pickle('smak0.pkl')


data.dir2=data.apply(lambda x: windir(x['dir']),axis=1)

"""
Gráficos
"""

fig, ax=plt.subplots(subplot_kw={'projection': 'windrose'})

ax.bar(data.dir2, data.M, normed=True, bins=[0,0.5,1,1.5], colors=('lightgrey','darkgrey','dimgrey','black')) 

ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
ax.legend(loc='lower right', decimal_places=1).set_title('M [m/s]')

fig.suptitle('Rosa de los vientos - SMAK-3 - prueba en puente')

fig.savefig('rosa_vientos_smak.pdf')