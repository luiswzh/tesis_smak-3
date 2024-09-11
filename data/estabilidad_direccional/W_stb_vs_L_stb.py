# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:45:45 2024

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

with open('eesresults.txt',newline='') as file:
    reader=csv.reader(file)
    next(reader)
    next(reader)
    x=list()
    y=list()
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[9]))
        

"Grafico"

fig, ax=plt.subplots()

ax.scatter(x,y,marker='s',color='0')
ax.scatter(x[24],y[24],marker='s', color='red', label='$L_{stb}=25$ cm')

ax.set_xlim([0, 0.35])
ax.set_ylim([0.01,0.035])

ax.set_ylabel(r'\ensuremath{W_{stb-total}}[kgf]')
ax.set_xlabel(r'\ensuremath{L_{stb}}[m]')

ax.set_title(r'$W_{stb-total}$ vs $L_{stb}$')
ax.legend()
fig.set_size_inches(w=5, h=4)

fig.savefig('W_vs_L_direccional.pdf')