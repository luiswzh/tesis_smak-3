# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:19:18 2024

@author: luisw
"""
import numpy as np
from iapws.iapws95 import IAPWS95_Tx as iapws

def elapsed_time(df):
    """
    Generate elapsed time column in df

    Parameters
    ----------
    df : DataFrame with datetime 'timestamp' column
    Returns
    -------
    DataFrame with elapsed time

    """
    initial_time=df['timestamp'][0]
    return df.apply(lambda x: x['timestamp']-initial_time, axis=1)

def valid_wind(df, h_dir=120, v_dir=15):
    """
    Checks if the wind direction is valid

    Parameters
    ----------
    df : dataframe with U,V,W wind components
    h_dir : optional
        maximum horizontal direction. The default is 120.
    v_dir : optional
        maximum vertical direction. The default is 15.

    Returns
    -------
    pandas DataFrame with True when wind is within boundaries, otherwise False
        

    """
    def is_valid(h,v):
        if(-h_dir<h<h_dir and -v_dir<v<v_dir):
            return True
        else:
            return False
    
    def calculate_directions(U,V,W):
        h=np.degrees(np.arctan2(U,-V))
        
        horizontal=np.sqrt(U**2+V**2)
        
        v=np.degrees(np.arctan2(W,horizontal))
        return h,v
    
    return df.apply(lambda x: is_valid(*calculate_directions(x['U'], x['V'], x['W'])), axis=1)

def specific_humidity(P,T,RH):
    """
    Calculates specific humidity

    Parameters
    ----------
    P : Pressure, hPa or mbar
    T : Temperature, C
    RH : relative humidity, 0-100

    Returns
    -------
    humidity : specific humidity, kg/kg

    """
    water_pressure=iapws(T+273.15,1).P*10000
    RH=RH/100
    humidity=(0.622*RH*water_pressure)/(P-RH*water_pressure)
    
    return humidity

def potential_temperature(P,T,P0=1000):
    """
    Calculates potential temperature

    Parameters
    ----------
    P : Pressure, hPa or mbar
    T : Temperature, C
    P0 : optional
        Reference pressure, hPa or mbar. The default is 1000.

    Returns
    -------
    T_pot : Potential temperature, C
    
    """
    T_pot=(T+273.15)*((P0/P)**0.286)
    T_pot=T_pot-273.15
    return T_pot
    
def virtual_temperature(T_pot,hum):
    """
    Calculates virtual temperature

    Parameters
    ----------
    T_pot : Potential temperature, C
    hum : specific humidity, kg/kg or g/g

    Returns
    -------
    T_virtual : Virtual temperature, C

    """
    T_virtual=(T_pot+273.15)*(1+0.61*hum)
    T_virtual=T_virtual-273.15
    return T_virtual

def wind_direction(X,Y):
    """
    Calculates wind direction from X to Y

    Parameters
    ----------
    X : X wind, north component
    Y : Y wind, east component

    Returns
    -------
    direction : wind direction, degrees

    """
    direction=np.degrees(np.arctan2(Y,X))
    return direction