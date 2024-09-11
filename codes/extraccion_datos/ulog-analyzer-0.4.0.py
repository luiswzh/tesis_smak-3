# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 14:05:49 2024

@author: luisw

Script to process ulog file into a dataframe containing a set of reduced
variables at a give frequency.
"""

import pandas as pd
import px4tools as px
import tkinter as tk
from tkinter import filedialog as fd

from scipy.spatial.transform import Rotation as R
import math

"Configuration"
root=tk.Tk()
root.withdraw() #Hides main window

#File directories
#Input
file_path = fd.askopenfilename()


#Output
#path_output = fd.askdirectory()

#Times
#init time
#time_init = time.datetime(2024,2,12,16,48,00)

#frequency (for data merging) (use period 1/f)
freq = 0.1

#Parameters to extract dictionary, key should be the desired header and value the codified name in ulog

variable_list = {
    "roll":"t_vehicle_attitude_0__f_roll",
    "pitch":"t_vehicle_attitude_0__f_pitch",
    "yaw":"t_vehicle_attitude_0__f_yaw",
    "g1":"t_vehicle_angular_velocity_0__f_xyz_0_",
    "g2":"t_vehicle_angular_velocity_0__f_xyz_1_",
    "g3":"t_vehicle_angular_velocity_0__f_xyz_2_",
    "a1":"t_vehicle_acceleration_0__f_xyz_0_",
    "a2":"t_vehicle_acceleration_0__f_xyz_1_",
    "a3":"t_vehicle_acceleration_0__f_xyz_2_",
    "m1":"t_vehicle_magnetometer_0__f_magnetometer_ga_0_",
    "m2":"t_vehicle_magnetometer_0__f_magnetometer_ga_1_",
    "m3":"t_vehicle_magnetometer_0__f_magnetometer_ga_2_",
    "P":"t_vehicle_air_data_0__f_baro_pressure_pa",
    "T":"t_vehicle_air_data_0__f_baro_temp_celcius",
    "unix-time":"t_sensor_gps_0__f_time_utc_usec",
    "alt":"t_vehicle_global_position_0__f_alt",
    "alt_rel":"t_vehicle_local_position_0__f_z",
    "lat":"t_vehicle_global_position_0__f_lat",
    "lon":"t_vehicle_global_position_0__f_lon",
    "vx":"t_vehicle_local_position_0__f_vx",
    "vy":"t_vehicle_local_position_0__f_vy",
    "vz":"t_vehicle_local_position_0__f_vz",
    }

"ULOG file processing with PX4Tools"
#step 1 reads ulg file into a PX4 dictionary:
a = px.read_ulog(file_path)

#step 2 concatenates data at conf frequency:
b = a.concat(dt=freq)

#step 3 computes roll, pitch, yaw on euler angles from quartenions
#c = px.compute_data(b)
def rotate(x):
    if math.isnan(x['t_vehicle_attitude_0__f_q_0_']):
        return [float('nan'),float('nan'),float('nan')]
    rot=R.from_quat([x['t_vehicle_attitude_0__f_q_1_'],x['t_vehicle_attitude_0__f_q_2_'],x['t_vehicle_attitude_0__f_q_3_'],x['t_vehicle_attitude_0__f_q_0_']])
    euler_rotated=rot.as_euler('xyz')
    return euler_rotated

c=b.copy()
rotation=c.apply(rotate , axis=1)

c["t_vehicle_attitude_0__f_roll"]=rotation.apply(lambda x: x[0])
c["t_vehicle_attitude_0__f_pitch"]=rotation.apply(lambda x: x[1])
c["t_vehicle_attitude_0__f_yaw"]=rotation.apply(lambda x: x[2])


"Tabular data building"

df = pd.DataFrame()

for key, value in variable_list.items():
    if value in c.columns:
        df[key]=c[value]
    else:
        print(str(value)+" not found")


"Extras"
#df['time-init-10hz']=pd.date_range(start=time_init,freq='0.1S',periods=df.shape[0]);

#df['roll_deg']=np.degrees(df['roll'])
#df['pitch_deg']=np.degrees(df['pitch'])
#df['yaw_deg']=np.degrees(df['yaw'])
df['time-utc']=pd.to_datetime(df["unix-time"],unit="us")

#filename=input("Output file name: ")
df.to_pickle(fd.asksaveasfilename())



