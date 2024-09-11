# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 21:43:16 2024

@author: luisw

Aceleraciones máximas presentadas en cada vuelo
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 10,
})

"""
Lectura de datos
"""

data=pd.read_pickle('data_px.pkl')

for df in data:
    df.dropna(inplace=True)
    df['a_magnitude']=df.apply(lambda x: np.linalg.norm([x['a1'],x['a2'],x['a3']]), axis=1)
    df.index=df.index-df.index[0]
    df.index=df.apply(lambda x: x.name.total_seconds()/60, axis=1)

"""
Graficado
"""

fig, ax= plt.subplots()

i=0
for df in data:
    ax.plot(df.index, df['a_magnitude'], linewidth=0.5, label=f'F0{i+1}')
    maxdata=df[df['a_magnitude']==df['a_magnitude'].max()]
    maxdata_value=maxdata['a_magnitude'].iloc[0]
    ax.annotate(f'F0{i+1}: {maxdata_value:.2f}', (maxdata.index[0], maxdata_value))
    
    ax.legend()
    
    i+=1

ax.set_xlabel('Tiempo [min]')
ax.set_ylabel('Aceleración [m/s$^2$]')

fig.suptitle('Aceleraciones registradas en los vuelos')

fig.set_size_inches(w=6, h=4)

fig.savefig('smak_acceleration.pdf')