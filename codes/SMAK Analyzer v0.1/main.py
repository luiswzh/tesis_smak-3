# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:00:42 2024

@author: luisw

Merge, synchronize, rotate, and calculate SMAK data

Requires smak and pixhawk data
"""

import tools.storage as storage
import tools.merge as merge
import tools.rotate as rotate
import tools.compute as compute
import tools.spectral as spectral
import tools.circular_stats as circular

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

"""
Configuration
"""
configuration=dict()

configuration['version']='0.1.0'

configuration['in_vectors']={
    "A":["AX","AY","AZ"],
    "G":["GX","GY","GZ"],
    "M":["MX","MY","MZ"],
    "WIND":["U","V","W"],
    "G_px":["g1_px","g2_px","g3_px"],
    "A_px":["a1_px","a2_px","a3_px"],
    "M_px":["m1_px","m2_px","m3_px"],
    "V_px":["vx_px","vy_px","vz_px"],
    }

configuration['transform']={
    "A":"NWD",
    "G":"NWD",
    "M":"SWD",
    "WIND":"ENU",
    "G_px":"NED",
    "A_px":"NED",
    "M_px":"NED",
    "tsm_pos":"NED",
    }

configuration['out_vectors']=['A','G','M','WIND','G_px','A_px','M_px','V_px','tsm_pos','V_tsm_v','V_tsm_rot','V_tsm','WIND_true']

configuration['tsm_position']=np.array([0.345,0,-0.05])

configuration['excluded_for_mean']=['timestamp','LAT','LNG','ALT','HR','MIN','SEC','CS','EC','timestamp_e','valid_wind','unix-time_px','time-utc_px','roll_cs','pitch_cs','yaw_cs']

configuration['plot']=dict()

def print_executing(func):
    def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@print_executing
def load_data():
    smak=storage.readfile("Select smak data file:")
    pixhawk=storage.readfile("Select pixhawk data file:")
    
    smak['timestamp_e']=compute.elapsed_time(smak)
    smak['valid_wind']=compute.valid_wind(smak)
    pixhawk.P=pixhawk.P/100
    
    configuration['offset']=merge.get_offset(smak,pixhawk)
    #configuration['offset']=8.5
    
    return merge.merge(smak, pixhawk, configuration['offset'])

@print_executing
def compute_sine_cosine(data):
    data["roll_cs"]=data.apply(lambda x: rotate.sine_cosine(x['roll_px']),axis=1)
    data["pitch_cs"]=data.apply(lambda x: rotate.sine_cosine(x['pitch_px']),axis=1)
    data["yaw_cs"]=data.apply(lambda x: rotate.sine_cosine(x['yaw_px']),axis=1)
    
    return data

@print_executing
def compute_rotation(data):
    data=rotate.merge_components(data, configuration['in_vectors'])
    data['tsm_pos']=data.apply(lambda x: configuration['tsm_position'], axis=1)
    
    for key, value in configuration['transform'].items():
        data[key]=data.apply(lambda x: rotate.rotate_toNED(x[key],value,roll_cs=x["roll_cs"],pitch_cs=x["pitch_cs"],yaw_cs=x["yaw_cs"]),axis=1)
  
    return data

@print_executing
def compute_wind(data):
    data["V_tsm_v"]=data["V_px"]
    data["V_tsm_rot"]=data.apply(lambda x: np.cross(x["G_px"],x["tsm_pos"]), axis=1)
    data["V_tsm"]=data["V_tsm_v"]+data["V_tsm_rot"]

    data["WIND_true"]=data["WIND"]+data["V_tsm"]
    return data

@print_executing
def compute_extra(data):
    data["specific_humidity"]=data.apply(lambda x: compute.specific_humidity(x['P'],x['T'],x['RH']),axis=1)
    data["T_pot"]=data.apply(lambda x: compute.potential_temperature(x['P'],x['T']),axis=1)
    data["T_virtual"]=data.apply(lambda x: compute.virtual_temperature(x['T_pot'],x['specific_humidity']),axis=1)
    data["wind_dir"]=data.apply(lambda x: compute.wind_direction(-x['WIND_true_x'],-x['WIND_true_y']),axis=1)
    if 'alt_px' in data:
        data['h']=data['alt_px']-data['alt_px'].min()
    elif 'alt_rel_px' in data:
        data['h']=data['alt_rel_px'].max()-data['alt_rel_px']
    return data   

@print_executing
def split_height(data, h_step, plot_stats=True):
    height_range=np.arange(data.h.min(),data.h.max(),h_step)
    group=data.groupby(pd.cut(data['h'],height_range), observed=True)
    group_st=data.drop(columns=configuration['excluded_for_mean']).groupby(pd.cut(data['h'],height_range), observed=True)
    group_mean=group_st.mean()
    group_std=group_st.std()
    stat_df=pd.DataFrame()
    stat_df['h_mean']=group_mean['h']
    
    circular_list={
        "roll_px":[-np.pi, np.pi],
        "pitch_px":[-np.pi, np.pi],
        "yaw_px":[-np.pi, np.pi],
        "roll_deg_px":[-180, 180],
        "pitch_deg_px":[-180, 180],
        "yaw_deg_px":[-180, 180],
        "wind_dir":[-180, 180]
        }
    
    for variable, crange in circular_list.items():
        group_mean[variable]=circular.mean(group_st[variable],crange)
        group_std[variable]=circular.std(group_st[variable],crange)
    
    #WIND without out of range values
    filtered_data=data[data['valid_wind']]
    group_st_f=filtered_data.drop(columns=configuration['excluded_for_mean']).groupby(pd.cut(filtered_data['h'],height_range), observed=True)
    
    for column in group_mean.columns:
        if 'WIND' in column.upper():
            group_mean[column]=group_st_f[column].mean()
            group_std[column]=group_st_f[column].std()
        stat_df[column+"_mean"]=group_mean[column]
        stat_df[column+"_std"]=group_std[column]
        if plot_stats:
            fig, ax = plt.subplots()
            ax.errorbar(stat_df[column+"_mean"], stat_df['h_mean'], xerr=stat_df[column+"_std"], fmt='--o')
            fig.suptitle('altitude vs '+str(column), y=0.95)
            ax.set_ylabel('Altitude [m]')
            ax.set_xlabel(str(column))
            ax.grid()
            configuration['plot'][column]=(fig,ax)
    
    stat_df['data_count']=group_st.P.count()
    stat_df['data_count_filtered']=group_st_f.P.count()
    stat_df['wind_data_loss_percentage']=(stat_df['data_count']-stat_df['data_count_filtered'])/stat_df['data_count']*100
    
    return group, stat_df.copy()

@print_executing
def add_TI(data):
    data["TI"]=data["WIND_true_magnitude_std"]/data["WIND_true_magnitude_mean"]
    data["TI_x"]=data["WIND_true_x_std"]/data["WIND_true_magnitude_mean"]
    data["TI_y"]=data["WIND_true_y_std"]/data["WIND_true_magnitude_mean"]
    data["TI_z"]=data["WIND_true_z_std"]/data["WIND_true_magnitude_mean"]
    
    fig, ax = plt.subplots()
    ax.plot(data["TI"], data['h_mean'], '--o')
    fig.suptitle('altitude vs turbulence intensity', y=0.95)
    ax.set_ylabel('Altitude [m]')
    ax.set_xlabel('turbulence intensity')
    ax.grid()
    configuration['plot']["TI"]=(fig,ax)
    
    return data

@print_executing
def spectra_analysis(df_group):
    spectra=dict()
    for name, group in df_group:
        spectra[name]=spectral.compute(group, 'WIND '+str(name)+'m')
        configuration['plot']['wind spectra '+str(name)]=(spectra[name][0],spectra[name][1])
    
    return spectra

def save_analysis(stat_in_excel=True):
    storage.savefile(configuration,'Save configuration')
    storage.savefile(data, 'Save data')
    storage.savefile(data_height_stat, 'Save stats data')
    storage.save_plots(configuration['plot'])
    if stat_in_excel:
        storage.savefile_xlsx(data_height_stat, 'Save stats data in excel')
    
if __name__ == "__main__":
    print("SMAK Data Analyzer v"+configuration['version'])
    
    data=load_data()
    
    data=data.dropna()
    
    data=compute_sine_cosine(data)

    data=compute_rotation(data)
    
    data=compute_wind(data)
    
    data=rotate.expand_vectors(data, configuration['out_vectors'])
    
    data=compute_extra(data)
    
    data_height, data_height_stat=split_height(data, 5)
    
    data_height_stat=add_TI(data_height_stat)
    
    spectra=spectra_analysis(data_height)
    
    
    
    