# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:11:40 2024

@author: luisw

Gráfico de volumen de helio perdido

Periodo 1
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from scipy.stats import linregress


matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

"""
Lectura de datos
"""
data=pd.read_excel('periodo1.xlsx')

"""
Cáculos
"""
data['flotacion']=data['contrapeso']-data['globo_contrapeso']
data['flotacion_lost']=data['flotacion'].iloc[0]-data['flotacion']
data['volumen_helio_perdido']=data['flotacion_lost']/(data['rho_aire']-data['rho_helio'])/1000


"""
Regresión lineal
"""
regresion=linregress(data['deltatime'],data['volumen_helio_perdido'])

"""
Graficado
"""

fig, ax = plt.subplots()


ax.plot(data['deltatime'], regresion.intercept+regresion.slope*data['deltatime'], '--', color='0.3', label=f'$y={regresion.slope:.4f}x{regresion.intercept:.4f}$; $r^2={regresion.rvalue**2:.4f}$')

ax.scatter(data['deltatime'],data['volumen_helio_perdido'], marker='s', color='0')

ax.legend()

fig.suptitle('Volumen de helio perdido en periodo de 29-feb a 8-mar')
ax.set_xlabel('Tiempo transcurrido desde llenado [días]')
ax.set_ylabel('Volumen total perdido [m$^3$]')

fig.set_size_inches(w=5, h=4)

fig.savefig('helio_periodo1.pdf')