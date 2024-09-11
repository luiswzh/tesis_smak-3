# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 13:15:43 2024

@author: luisw

Gráfico de prueba con giro
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Computer Modern Roman',
    'text.usetex': True,
    'font.size': 8,
})

def expand_vectors(df1):
    """
    Returns a dataframe with vector on a single column to 3 components on their own column
    
    Parameters
    ----------
    df1 : dataframe containing the vectors
    var_list : list of vectors to expand

    Returns
    -------
    df2 : dataframe with expanded vectors (eg: V --> Vx,Vy,Vz)

    """
    var_list=['A','G','M','WIND','G_px','A_px','M_px','V_px','tsm_pos','V_tsm_v','V_tsm_rot','V_tsm','WIND_true']
    df2=df1.copy()
    for value in var_list:
        df2[value+"_x"]=df2.apply(lambda x: x[value][0],axis=1)
        df2[value+"_y"]=df2.apply(lambda x: x[value][1],axis=1)
        df2[value+"_z"]=df2.apply(lambda x: x[value][2],axis=1)
        df2[value+"_magnitude"]=df2.apply(lambda x: np.linalg.norm(x[value]),axis=1)
    df2.drop(labels=var_list,axis=1,inplace=True)
    return df2

"""
Lectura de datos
"""
data=expand_vectors(pd.read_pickle('datos_giro.pkl'))
data['time']=data.apply(lambda x: x['timestamp_e'].total_seconds()/60, axis=1)

"""
Filtros
"""
data.dropna(inplace=True)


"""
Graficado
"""
fig, ax = plt.subplots()

ax.plot(data.time,data.WIND_magnitude,label='medido')
ax.plot(data.time,data.WIND_true_magnitude,label='calculado')


ax.legend()


ax.set_xlim([0,8.5])
ax.set_ylim([0,4])

ax.set_ylabel(r'Magnitud de viento [m/s]')
ax.set_xlabel(r'Tiempo [min]')
ax.legend()
ax.set_title(r'Comparación de viento calculado con viento medido')

fig.set_size_inches(w=5, h=4)

fig.savefig('wind_gyro_test.pdf')





