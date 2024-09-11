# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:18:52 2024

@author: luisw
"""

import datetime as dt

from scipy.optimize import minimize_scalar as minimize

import matplotlib.pyplot as plt

from tools.euler_interpolation import slerp_euler

import numpy as np

import math

def get_value(x, sr, offset=0, check_range=False):
    lookval=x+dt.timedelta(seconds=offset)
    if(check_range):
        if(lookval<sr.index[0]):
            return float('nan')
        elif(lookval>sr.index[-1]):
            return float('nan')
    
    if(lookval<sr.index[0]):
        return sr.iloc[0]
    elif(lookval>sr.index[-1]):
        return sr.iloc[-1]
    
    upper=sr[sr.index>=lookval].head(1)
    lower=sr[sr.index<=lookval].tail(1)
    
    x0=lower.index[0].total_seconds()
    x1=upper.index[0].total_seconds()
    y0=lower.iloc[0]
    y1=upper.iloc[0]
    
    """
    if(math.isnan(y0) or math.isnan(y1)):
        return float('nan')
    """
    if isinstance(y0, dt.datetime):
        if y0.microsecond == 0:
            return y0
    
    lookval=lookval.total_seconds()

    if(x0==x1):
        return y0
    
    y=y0+((y1-y0)/(x1-x0))*(lookval-x0)
    
    return y

def get_value_rot(x, sr_roll, sr_pitch, sr_yaw, offset=0, check_range=False):
    #print(x)
    lookval=x+dt.timedelta(seconds=offset)
    sr=sr_roll
    if(check_range):
        if(lookval<sr.index[0]):
            return [float('nan'),float('nan'),float('nan')]
        elif(lookval>sr.index[-1]):
            return [float('nan'),float('nan'),float('nan')]
    
    if(lookval<sr.index[0]):
        return sr.iloc[0]
    elif(lookval>sr.index[-1]):
        return sr.iloc[-1]
    
    upper=sr[sr.index>=lookval].head(1)
    lower=sr[sr.index<=lookval].tail(1)
    
    x0=lower.index[0].total_seconds()
    x1=upper.index[0].total_seconds()
    
    y0_roll=lower.iloc[0]
    y1_roll=upper.iloc[0]
    
    sr=sr_pitch
    upper=sr[sr.index>=lookval].head(1)
    lower=sr[sr.index<=lookval].tail(1)
    
    y0_pitch=lower.iloc[0]
    y1_pitch=upper.iloc[0]
    
    sr=sr_yaw
    upper=sr[sr.index>=lookval].head(1)
    lower=sr[sr.index<=lookval].tail(1)
    
    y0_yaw=lower.iloc[0]
    y1_yaw=upper.iloc[0]
    
    y0=[y0_roll,y0_pitch,y0_yaw]
    y1=[y1_roll,y1_pitch,y1_yaw]
    
    for value in y0:
        if math.isnan(value):
            return [float('nan'),float('nan'),float('nan')]
    
    for value in y1:
        if math.isnan(value):
            return [float('nan'),float('nan'),float('nan')]
    
    lookval=lookval.total_seconds()

    if(x0==x1):
        return y0
    
    y=slerp_euler(lookval, x0, x1, y0, y1)
    
    return y

def get_offset(A,B,criteria='P'):
    def diff_sum(offset):
        df=A.copy()
        df=df.set_index('timestamp_e')
        df=df.resample('1S').nearest()
        df[criteria+"_B"]=df.apply(lambda x: get_value(x.name,B[criteria],offset), axis=1)
        df["diff"]=df.apply(lambda x: abs(x[criteria]-x[criteria+"_B"]), axis=1)
        print(df["diff"].sum())
        print(offset)
        return df["diff"].sum()
    #offset=minimize(diff_sum, tol=0.0001)
    def plot_data():
        plt.plot(A['timestamp_e']/1e9, A[criteria], label="smak")
        plt.plot(B.index/1e9, B[criteria], label="pixhawk")
        plt.suptitle('look for offset', y=0.95)
        plt.legend()
        plt.show()
        while plt.fignum_exists(1):
           plt.pause(0.1)
    
    plot_data()
    """
    plot_thread = threading.Thread(target=plot_data)
    plot_thread.start()
    plot_thread.join()
    """
    
    print("Please input A<B<C range for offset lookup")
    a=float(input("A: "))
    b=float(input("B: "))
    c=float(input("C: "))
    
    offset=minimize(diff_sum, tol=0.0000001, bracket=(a,b,c))
    
    
    if(offset.success):
        return offset.x
    else:
        print('Error getting offset')
        return False

def merge(A,B,offset):
    rots=['roll','pitch','yaw']
    df=A.copy()
    for column in B.columns:
        if column not in rots:
            print('Adding '+str(column))
            df[column+"_px"]=df.apply(lambda x: get_value(x['timestamp_e'],B[column],offset, True), axis=1)
    
    print('Adding rotations')
    interpolated_rots=df.apply(lambda x: get_value_rot(x['timestamp_e'],B['roll'],B['pitch'],B['yaw'],offset, True), axis=1)
    df['roll_px']=interpolated_rots.apply(lambda x: x[0])
    df['pitch_px']=interpolated_rots.apply(lambda x: x[1])
    df['yaw_px']=interpolated_rots.apply(lambda x: x[2])
    
    df['roll_deg_px']=np.degrees(df['roll_px'])
    df['pitch_deg_px']=np.degrees(df['pitch_px'])
    df['yaw_deg_px']=np.degrees(df['yaw_px'])
    
    return df