# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:22:42 2024

@author: luisw

Gráfico de humedad relativa vs altura en bloques de 5 m
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

"""
Graficado
"""

fig, axes = plt.subplots(2,3)

fig.suptitle('Perfil de humedad relativa')
fig.supxlabel('Humedad relativa [\%]')
fig.supylabel('Altitud AGL [m]')

i=0
for ax in axes.flatten():
    ax.set_xlim([40, 60])
    ax.set_ylim([0,100])
    ax.set_xticks([40, 45, 50, 55, 60])
    ax.set_axisbelow(True)
    ax.grid()
    
    ax.set_title(f'F0{i+1}')
    ax.scatter(smak[i].iloc[1:]['RH_mean'], smak[i].iloc[1:]['h_mean'], marker='s', color='0', s=5, label='SMAK')
    
    i=i+1
    
for ax in axes[0]:
    ax.set_xticklabels([])
    
for i in range(2):
    axes[0][i+1].set_yticklabels([])
    axes[1][i+1].set_yticklabels([])



axes[0][2].legend()

fig.set_size_inches(w=6, h=5)

fig.savefig('profile_humidity.pdf')