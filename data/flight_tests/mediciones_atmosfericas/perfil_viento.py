# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:10:31 2024

@author: luisw

Gráfico de viento vs altura en bloques de 5 m
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

smak=pd.read_pickle('smak_stat.pkl')
young=pd.read_pickle('young_data.pkl')

"""
Graficado
"""

fig, axes = plt.subplots(2,3)

fig.suptitle('Perfil de viento')
fig.supxlabel('Viento [m/s]')
fig.supylabel('Altitud AGL [m]')

i=0
for ax in axes.flatten():
    ax.set_xlim([0,12])
    ax.set_ylim([0,100])
    ax.set_xticks([0, 3, 6, 9, 12])
    ax.set_axisbelow(True)
    ax.grid()
    
    ax.set_title(f'F0{i+1}')
    ax.scatter(smak[i].iloc[1:]['WIND_true_magnitude_mean'], smak[i].iloc[1:]['h_mean'], marker='s', color='0', s=5, label='SMAK')
    
    ax.scatter(young[i]['wind'].mean(),2,marker='^', color='0', s=8, label='YOUNG')
    
    i=i+1
    
for ax in axes[0]:
    ax.set_xticklabels([])
    
for i in range(2):
    axes[0][i+1].set_yticklabels([])
    axes[1][i+1].set_yticklabels([])



axes[0][2].legend(loc='upper left')

fig.set_size_inches(w=6, h=5)

fig.savefig('profile_wind.pdf')
