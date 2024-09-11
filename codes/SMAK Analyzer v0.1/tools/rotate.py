# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:19:12 2024

@author: luisw
"""

import pandas as pd
import numpy as np

def merge_components(df1, var_dict):
    """
    Returns a modified dataframe where individual components are turned to vector/array
    
    Args:
        df1: dataframe containing data
        var_dict: dictionary of vector and component name in df e.g.: "Speed":["Vx","Vy","Vz"]
        
    Returns:
        df2: modified dataframe with on column for each vector
    """
    df2=df1.copy()
    
    for key, value in var_dict.items():
        df2[key]=df2.apply(lambda x: np.array([x[component] for component in value]), axis=1)
        
        for component in value:
            df2=df2.drop(component, axis=1)
            
    return df2

def expand_vectors(df1, var_list, del_old=True):
    """
    Returns a dataframe with vector on a single column to 3 components on their own column and magnitude
    
    Parameters
    ----------
    df1 : dataframe containing the vectors
    var_list : list of vectors to expand

    Returns
    -------
    df2 : dataframe with expanded vectors and magnitude(eg: V --> Vx,Vy,Vz,V_magnitude)

    """
    df2=df1.copy()
    for value in var_list:
        df2[value+"_x"]=df2.apply(lambda x: x[value][0],axis=1)
        df2[value+"_y"]=df2.apply(lambda x: x[value][1],axis=1)
        df2[value+"_z"]=df2.apply(lambda x: x[value][2],axis=1)
        df2[value+"_magnitude"]= df2.apply(lambda x: np.linalg.norm(x[value]),axis=1)
        if del_old:
            df2=df2.drop(value, axis=1)
    
    return df2

def sine_cosine(angle, degree=False):
    """
    Parameters
    ----------
    angle: roll, pitch, or yaw angle in radians (degrees if degree=True)
    
    degree: True if the input is in degrees, otherwise False
    
    Returns
    -------
    sine
    cosine
    """
    
    if(degree):
        angle=np.degrees(angle)
    
    sine=np.sin(angle)
    cosine=np.cos(angle)
    
    return sine, cosine

def rotate_toNED(vector, frame, **kwargs):
    """
    Rotates vector to NED inertial frame

    Parameters
    ----------
    vector : 3D vector to be rotated
    frame : initial body fixed frame in 3 letter str format
            -first digit correspond to x direction
            -second digit correspond to y direction
            -third digit correspond to z direction
            
            *N(north):forward direction
            *E(east):right direction
            *S(south):rear direction
            *W(west):left direction
            *U(up):up direction
            *D(down):down direction
    
    Keyword args:
    -------------
    roll : roll angle of the frame
    pitch : pitch angle of the frame
    yaw : yaw angle of the frame
    
    roll_sc : sine and cosine of roll
    pitch_sc : sine and cosine of pitch
    yaw_sc : sine and cosine of yaw
    
    **one set of kwargs should be provided
    
    Returns
    -------
    rotated_vector : rotated 3D vector 

    """
    if not(len(frame)==3):
        print("Frame can only have 3 digits")
        return float('NaN')
    
    #Step 1: fixes to FRD body frame
    
    frd_vector=np.zeros(3)
    
    for index, direction in enumerate(frame):
        value=vector[index]
        if(direction=="N"):
            frd_vector[0]=value
        elif(direction=="E"):
            frd_vector[1]=value
        elif(direction=="S"):
            frd_vector[0]=-value
        elif(direction=="W"):
            frd_vector[1]=-value
        elif(direction=="U"):
            frd_vector[2]=-value
        elif(direction=="D"):
            frd_vector[2]=value
        else:
            print("Invalid direction")
            return float('NaN')
    
    vector=frd_vector
    
    #Step 2: computes sines and cosines
    angles={"roll","pitch","yaw"}
    cs={"roll_cs","pitch_cs","yaw_cs"}
    
    if(kwargs.keys() >= cs):
        r_s,r_c=kwargs["roll_cs"]
        p_s,p_c=kwargs["pitch_cs"]
        y_s,y_c=kwargs["yaw_cs"]
        
    elif(kwargs.keys() >= angles):
        r_s,r_c=sine_cosine(kwargs["roll"])
        p_s,p_c=sine_cosine(kwargs["pitch"])
        y_s,y_c=sine_cosine(kwargs["yaw"])
        
    else:
        print("Insufficient rotation info")
        return float('NaN')
    
    #Step 3: Compute rotation matrix and rotate
    c,s=r_c,r_s
    r_t=np.transpose(np.array([[1,0,0],
                               [0,c,s],
                               [0,-s,c]]))
    c,s=p_c,p_s
    p_t=np.transpose(np.array([[c,0,-s],
                               [0,1,0],
                               [s,0,c]]))
    c,s=y_c,y_s
    y_t=np.transpose(np.array([[c,s,0],
                               [-s,c,0],
                               [0,0,1]]))
    
    rotated_vector=np.matmul(r_t,vector) #roll rotation
    rotated_vector=np.matmul(p_t,rotated_vector) #pitch rotation
    rotated_vector=np.matmul(y_t,rotated_vector) #yaw rotation
    
    return rotated_vector