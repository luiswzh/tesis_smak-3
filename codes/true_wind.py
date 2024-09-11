# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:47:27 2024

@author: luisw

Programa para calcular el viento real

Datos requeridos:
    -Viento medido (body->right-forward-up)
    -Velocidad pixhawk (t_vehicle_local_position_0) (inertial->north-east-down)
    -Velocidad angular pixhawk (t_vehicle_angular_velocity_0__f_xyz) (body->forward-right-down)
    -Angulos de actitud, pixhawk (roll, pitch, yaw)

"""
import numpy as np

def valid_wind(wind, h_dir=120, v_dir=15):
    """
    Checks if the measured wind is within valid range

    Parameters
    ----------
    wind : np.array
        measured wind
    h_dir : int, optional
        Maximum accepted wind angle in horizontal direction. The default is 120.
    v_dir : int, optional
        Maximum accepted wind angle in vertical direction. The default is 15.

    Returns
    -------
    bool
        True if wind is within accepted range otherwise False

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
    
    return is_valid(*calculate_directions(wind[0],wind[1],wind[2]))

def sine_cosine(angle, degree=False):    
    """
    Compute sine and cosine of an angle

    Parameters
    ----------
    angle : float
        Angle in radians (in degress if degree=True).
    degree : bool, optional
        use True if the angle is in degrees. The default is False.

    Returns
    -------
    sine : float
        sine of angle.
    cosine : float
       cosine of angle.

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

def calculate_true_wind(measured_wind, velocity, angular_velocity, euler_angles, wind_filter):
    """
    Calculate true wind

    Parameters
    ----------
    measured_wind : np.array
        Measured wind in right-forward-up. m/s
    velocity : np.array
        Velocity in north-east-down. m/s
    angular_velocity : np.array
        Angular velocity in forward-right-down. m/s
    euler_angles : np.array
        Euler angles -> roll, pitch, yaw. radians
    wind_filter : bool
        True if wind filtering is needed.

    Returns
    -------
    true_wind : np.array
        True wind in north-east-down. m/s

    """
    #Checks if measured wind is within range
    if wind_filter and not valid_wind(measured_wind):
        return None
    
    #Constants
    tsm_position=np.array([0.345,0,-0.05]) #position in forward-right-down
    
    #Compute sine-cosine
    roll_cs=sine_cosine(euler_angles[0])
    pitch_cs=sine_cosine(euler_angles[1])
    yaw_cs=sine_cosine(euler_angles[2])
    
    #Rotations
    measured_wind=rotate_toNED(measured_wind, 'ENU', roll_cs=roll_cs,pitch_cs=pitch_cs,yaw_cs=yaw_cs)
    
    angular_velocity=rotate_toNED(angular_velocity, 'NED', roll_cs=roll_cs,pitch_cs=pitch_cs,yaw_cs=yaw_cs)
    
    tsm_position=rotate_toNED(tsm_position, 'NED', roll_cs=roll_cs,pitch_cs=pitch_cs,yaw_cs=yaw_cs)
    
    #Calculate sensor velocity

    tsm_velocity=velocity+np.cross(angular_velocity, tsm_position)
    
    #Calculate true wind
    true_wind=measured_wind+tsm_velocity
      
    return true_wind

def calculate(state, wind_filter=True):
    """
    calculate true wind

    Parameters
    ----------
    state : object
        Contains attributes:
            -M: wind vector
            -V: velocity vecto
            -w: angular velocity vector
            -angles: array with roll, pitch, and yaw.
    wind_filter : bool, optional
        True if wind filtering is needed. The default is True.

    Returns
    -------
    np.array
        True wind vector.

    """
    return calculate_true_wind(state.M, state.V, state.w, state.angles, wind_filter)


if __name__=="__main__":
    print('True wind calculator test')
    
    class state:
        def __init__(self, M, V, w, angles):
            self.M=M
            self.V=V
            self.w=w
            self.angles=angles
        
    #Tests
    test1={
        'M':np.array([1.08,-0.06,-0.24]),
        'V':np.array([-0.511857,0.814148,0.0960109]),
        'w':np.array([0.310934,0.0348527,-1.04684]),
        'angles':np.array([-0.0310506,0.00561535,-2.74526])
        }
    test1=state(test1['M'],test1['V'],test1['w'],test1['angles'])
    
    test1_expected=np.array([-0.170624,0.155243,0.301468])
    
    test2={
        'M':np.array([0.38,-0.43,0.05]),
        'V':np.array([0.0352689,1.11914,0.199667]),
        'w':np.array([-0.0530996,-0.653336,-2.07332]),
        'angles':np.array([0.0590521,0.0488007,1.34895])
        }
    test2=state(test2['M'],test2['V'],test2['w'],test2['angles'])
    test2_expected=np.array([0.287826,0.659756,0.37419])
    
    test1_calc=calculate(test1)
    test2_calc=calculate(test2)
    
    print('Test 1 expected value is: '+str(test1_expected))
    print('Test 1 calculated value is: '+str(test1_calc))
    
    print('Test 2 expected value is: '+str(test2_expected))
    print('Test 2 calculated value is: '+str(test2_calc))
    
    