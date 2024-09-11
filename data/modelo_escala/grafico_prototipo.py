# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 20:23:46 2024

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
        x.append(float(row[6]))
        y.append(float(row[5]))

"Regresion polinomial"        
def modelopoli(x):
    a2=0.0441
    a1=-0.318
    a0=0.5055
    return a2*(x**2)+a1*x+a0
"Grafico"

fig, ax=plt.subplots()

#ax.scatter(x,y,marker='s',color='0')
x1=np.linspace(0,24,100)
ax.plot(x1,list(map(modelopoli,x1)),label='regresión polinómica')

ax.set_xlim([0,25])
ax.set_ylim([0,25])

ax.set_ylabel(r'\ensuremath{\Theta}[deg]')
ax.set_xlabel(r'\ensuremath{V_{\infty}}[m/s]')
ax.legend()
ax.set_title(r'$\Theta$ vs $V_{\infty}$ - esperado en prototipo')

fig.set_size_inches(w=5, h=4)

fig.savefig('cabeceo_prototipo.pdf')