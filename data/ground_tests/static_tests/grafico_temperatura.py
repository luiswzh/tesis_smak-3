# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:33:33 2024

@author: luisw

Gráfico de temperatura en prueba estática
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from datetime import datetime, date

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

"""
Lectura de datos
"""
manual=pd.read_pickle('manual-log.pkl')
smak=pd.read_pickle('smak_static_test.pkl')

"""
Cálculo de tiempo relativo
"""
manual['t_delta']=manual.apply(lambda x: (datetime.combine(date.today(),x.name)-datetime.combine(date.today(), manual.index[0])).total_seconds()/60, axis=1)
smak['t_delta']=smak.apply(lambda x: (x.timestamp-smak.timestamp.iloc[0]).total_seconds()/60, axis=1)


"""
Gráficos
"""
fig, ax=plt.subplots()

ax.plot(manual.t_delta,manual.temperature, ':o', color='0', label='Barotermohigrómetro')
ax.plot(smak.t_delta,smak['T'],color='0', label='SMAK-3')

#ax.set_xlim([0,60])
#ax.set_ylim([995,1005])

ax.set_ylabel(r'Temperatura [$^\circ$C]')
ax.set_xlabel(r'Tiempo [min]')
ax.legend()
ax.set_title(r'Prueba estática - Comparación de temperatura')

fig.set_size_inches(w=5, h=4)

fig.savefig('prueba_estatica_temperatura.pdf')