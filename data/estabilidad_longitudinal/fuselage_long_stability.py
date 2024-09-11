# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:36:11 2024

@author: luisw
"""

import matplotlib.pyplot as plt
import matplotlib
import csv
from matplotlib.ticker import FormatStrFormatter

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

"Lectura de datos"

with open('lon_stb_fuselage.txt',newline='') as file:
    reader=csv.reader(file)
    next(reader)
    x=list()
    y=list()
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[2]))
        
"Regresion lineal"

m=-0.0081

"Grafico"

fig, ax=plt.subplots()

ax.scatter(x,y,marker='s',color='0')
ax.plot(x,[m*a for a in x],'--',label='regresión lineal')

ax.set_xlim([-11,11])
ax.set_ylim([-0.1,0.1])

ax.set_ylabel(r'\ensuremath{M_{fus}}[Nm]')
ax.set_xlabel(r'\ensuremath{\alpha}[deg]')
ax.legend()
ax.set_title(r'$M_{fus}$ vs $\alpha$')
ax.set_yticks([x/100 for x in range(-10,11,2)])

fig.set_size_inches(w=5, h=4)

fig.savefig('M_fus_lon.pdf')