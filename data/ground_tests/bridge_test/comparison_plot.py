# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:05:43 2024

@author: luisw

Gráfico de comparación

"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

"""
Lectura de datos
"""
smak=pd.read_pickle('smak_rotated.pkl')
young=pd.read_pickle('young_rotated.pkl')

"""
Cálculo de tiempo relativo
"""
smak.index=smak.index/60
young.index=young.index/60
"""
Gráficos
"""

fig, ax= plt.subplots(3)

#Gráfico de u
ax[0].plot(young.index,young.u, linewidth=0.3)
ax[0].plot(smak.index,smak.u, linewidth=0.3)

ax[0].set_ylabel('u [m/s]')
ax[0].set_xticks([])

#Gráfico de v
ax[1].plot(young.index,young.v, linewidth=0.3)
ax[1].plot(smak.index,smak.v, linewidth=0.3)

ax[1].set_ylabel('v [m/s]')
ax[1].set_xticks([])

#Gráfico de M
ax[2].plot(young.index,young.M,label='YOUNG81000', linewidth=0.3)
ax[2].plot(smak.index,smak.M,label='SMAK-3', linewidth=0.3)

ax[2].legend(loc='upper center')
ax[2].set_ylabel('M [m/s]')
ax[2].set_xlabel('Tiempo [min]')

#Detalles del gráfico
for a in ax:
    a.set_xlim([0,70])
    
fig.suptitle('Comparación de vientos medidos')
fig.set_size_inches(w=5, h=4)

fig.savefig('comparacion_vientos.pdf')