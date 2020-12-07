#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 19:51:14 2020

@author: benjamin
"""




#from TST_fun import writeNetCDF
import os
experiment = "TAS2"
import numpy as np
import pandas as pd
import time
import copy
#datapath = "/media/benjamin/Seagate_Drive1/TAS2/csv_TAS2/" 

outpath = "D:/TAS2/csv_min_mean/"


fld = os.listdir(datapath)
fld = sorted(fld, key = lambda x: int(x))






def readcsvtoarr2(datapath_csv_files,start_img=0,end_img=0,interval=1, fls = []):
    
    if len(fls) == 0:
        fls = os.listdir(datapath_csv_files)
        fls = sorted(fls, key = lambda x: x.rsplit('.', 1)[0])
        
    if end_img == 0:
        end_img = len(fls)-1
    
    counter = 0
    
    for i in range(start_img,end_img, interval): 
        i = 0
        if counter%10 == 0:
            print(str(counter)+" of "+str((end_img-start_img)/interval))
        #my_data = np.genfromtxt(datapath_csv_files+fls[i], delimiter=',', skip_header=1)
        #my_data = np.reshape(my_data,(1,my_data.shape[0],my_data.shape[1]))
        try:
            df = pd.read_csv(datapath_csv_files+fls[i],skiprows=1, delimiter=",", decimal=",")
            my_data = df.values
            my_data = np.reshape(my_data,(1,my_data.shape[0],my_data.shape[1]))
            if counter == 0:
                org_data = copy.copy(my_data)
            else:
                org_data = np.append(org_data,my_data,0)
            #org_data[counter] = my_data
        except  Exception as e:
            print(e)
            pass
        counter+=1
    
    return(org_data)
    
    





for j in range(2,23):
   
    fls = os.listdir(datapath+fld[j]+"/")
    start = time.time()
    if j == 2:
        start_for = 72900
    else:
        start_for = 0
    for i in range(start_for, len(fls), 1620):
       
        if i == 1620:      
            end = time.time()
            print(end - start) 
        print(i)
        follow_i = i+1620
        if follow_i > len(fls):
            follow_i = len(fls)
            
        
        tas1_arr = readcsvtoarr2(datapath_csv_files=datapath+fld[j]+"/",start_img=i,end_img=follow_i,interval=1)
        arr_steady = removeSteadyImages(tas1_arr, rec_feq = 27, print_out = True)
    
    
        avg = np.nanmean(arr_steady,axis=(0))
        np.savetxt(outpath+str(j)+"_"+str(i)+".csv", avg, delimiter=",")
    
import os
fls = os.listdir(outpath)
fls = [i for i in fls if i.endswith('.csv')]
fls = sorted(fls, key = lambda x: (int(x.split('.', 1)[0].split('_',1)[0]), int(x.rsplit('_', 1)[1].split('.',1)[0])))



minTAS1 = readcsvtoarr2(outpath, fls = fls, start_img=0,end_img=0)
minTAS1 = np.fliplr(minTAS1)

fls[1060]

outpath = "D:/TAS1/csv_min_mean_restart/"

writeNetCDF(outpath, "min_mean_TAS1_restart.nc", "Tb", minTAS1)


def readnetcdftoarr(datapath_to_file, var = 'Tb'):
    file = h5py.File(datapath_to_file,'r')
    arr = file.get(var)
    nparr = np.array(arr)
    return(nparr)

Tas2_1 = readnetcdftoarr(outpath+"min_mean_TAS1_1.nc")
Tas2_2 = readnetcdftoarr(outpath+"min_mean_TAS1_2.nc")


Tas2_1.shape
Tas2_2.shape

Tas2 = np.concatenate([Tas2_1, Tas2_2], 0)
writeNetCDF(outpath, "min_mean_TAS2.nc", "Tb", Tas2)
