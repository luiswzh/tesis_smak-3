# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 19:20:55 2024

@author: luisw
"""

import matplotlib.pyplot as plt
import matplotlib
import csv
import numpy as np

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

"Lectura de datos"

with open('resultados_modelo.txt',newline='') as file:
    reader=csv.reader(file)
    next(reader)
    x=list()
    y=list()
    for row in reader:
        x.append(float(row[4]))
        y.append(float(row[5]))

"Regresion polinomial"        
def modelopoli(x):
    a0=0.5055
    a1=-0.4498
    a2=0.0882
    return a2*(x**2)+a1*x+a0
"Grafico"

fig, ax=plt.subplots()

ax.scatter(x,y,marker='s',color='0')
x1=np.linspace(x[0],x[-1],100)
ax.plot(x1,list(map(modelopoli,x1)),'--',label='regresión polinómica')

ax.set_xlim([0,18])
ax.set_ylim([0,25])

ax.set_ylabel(r'\ensuremath{\Theta}[deg]')
ax.set_xlabel(r'\ensuremath{V_{\infty}}[m/s]')
ax.legend()
ax.set_title(r'$\Theta$ vs $V_{\infty}$ - Modelo a escala')

fig.set_size_inches(w=5, h=4)

fig.savefig('cabeceo_modelo.pdf')