# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:36:11 2024

@author: luisw
"""

import matplotlib.pyplot as plt
import matplotlib
import csv


matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

"Lectura de datos"

with open('dir_stb_fus.txt',newline='') as file:
    reader=csv.reader(file)
    next(reader)
    x=list()
    y=list()
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[2]))
        
"Regresion lineal"

m=-0.0161

"Grafico"

fig, ax=plt.subplots()

ax.scatter(x,y,marker='s',color='0')
ax.plot(x,[m*a for a in x],'--',label='regresión lineal')

ax.set_xlim([-18,18])
ax.set_ylim([-0.3,0.3])

ax.set_ylabel(r'\ensuremath{M_{fus}}[Nm]')
ax.set_xlabel(r'\ensuremath{\beta}[deg]')
ax.legend()
ax.set_title(r'$M_{fus}$ vs $\beta$')

fig.set_size_inches(w=5, h=4)

fig.savefig('M_fus_dir.pdf')