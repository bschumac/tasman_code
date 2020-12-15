#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:50:35 2020

@author: Benjamin Schumacher

Correct Sonic anemometer data using the planar fit algorithm of:
    https://github.com/bschumac/sonicfun
    
Before using this File, download the sonicfun package to make the tilt algorithm available. 
Run with Sonicfun as working directory
A example file is available with the sonicfun package as well. Therefore no detailed documentation here.


"""




from sonic_func import *
import numpy as np
import pandas as pd
import os
import copy

# create relative path variables
wd_path = "C:/PhD/Tasman_OP/"
#data_path = os.path.join(wd_path, "data")
example_file = os.path.join(wd_path, "smooth_cleaned.csv")

# read the data from the file
irg2 = pd.read_csv(example_file, header=[0,1], na_values='NAN')

for i in range(1,len(irg2),72000):
    if i%72000*5 == 0:
        print(i)
    if i+72000 < len(irg2):
        end_data = len(irg2)
    else:
        end_data = i+72000
        
    # cleaning the data from NANs and measurements from the day before
    timestamp = irg2["TIMESTAMP_UTC"].values[i:i+72000]
    u = irg2["Ux"].values[i:i+72000]
    v = irg2["Uy"].values[i:i+72000]
    w = irg2["Uz"].values[i:i+72000]
    Ts = irg2["Ts"].values[i:i+72000]
    CO2 = irg2["CO2"].values[i:i+72000]
    H2O = irg2["H2O"].values[i:i+72000]
    timestamp_pf, u1_pf, v1_pf, w1_pf, Ts_pf, CO2_pf, H2O_pf = planar_fit(u, v, w, sub_size = 10, timestamp = timestamp, Ts = Ts, H2O = H2O, CO2 = CO2)
    pf = pd.DataFrame({'TIMESTAMP': timestamp_pf.flatten(), 'Ux': u1_pf, 'Uy': v1_pf, 'Uz': w1_pf, 'Ts':Ts_pf.flatten(), 'CO2':CO2_pf.flatten(), 'H2O':H2O_pf.flatten()})
    if i == 1:
        pf_final = copy.copy(pf)
    else:
        pf_final = pf_final.append(pf) 

pf_final.to_csv(wd_path+"/smooth_cleaned_planarfit.csv")



# Example for tilt correction
#
timestamp_pf, u1_pf, v1_pf, w1_pf, Ts_pf, CO2_pf, H2O_pf = planar_fit(u, v, w, sub_size = 10, timestamp = timestamp, Ts = Ts, H2O = H2O, CO2 = CO2)
timestamp_rot3, u1_rot3, v1_rot3, w1_rot3 = triple_rot(u, v, w, sub_size = 10,timestamp=timestamp)

# Output from tilt correction to pandas dataframe
pf = pd.DataFrame({'TIMESTAMP': timestamp_pf.flatten(), 'Ux': u1_pf, 'Uy': v1_pf, 'Uz': w1_pf, 'Ts':Ts_pf.flatten(), 'CO2':CO2_pf.flatten(), 'H2O':H2O_pf.flatten()})
rot3 = pd.DataFrame({'TIMESTAMP': timestamp_rot3.flatten(), 'Ux': u1_rot3, 'Uy': v1_rot3, 'Uz': w1_rot3})

# write dataframe to file

rot3.to_csv(data_path+"/example_result_triplerotation.csv")