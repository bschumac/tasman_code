# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 20:57:25 2020

@author: benjamin.schumacher
"""




import numpy as np
import datetime
import pandas as pd
import os

from matplotlib import pyplot as plt 





def calcwinddirection(u,v): 
    
    erg_dir_rad = np.arctan2(u, v)
    erg_dir_deg = np.degrees(erg_dir_rad)
    erg_dir_deg_pos = np.where(erg_dir_deg < 0.0, erg_dir_deg+360, erg_dir_deg)

    return(np.round(erg_dir_deg_pos,2))


def calcwindspeed(v,u): 
    ws = np.sqrt((u*u)+(v*v))
    return(np.round(ws,2))



# create relative path variables
wd_path = "C:/PhD/Tasman_OP/"
#data_path = os.path.join(wd_path, "data")
example_file = os.path.join(wd_path, "smooth_cleaned_planarfit.csv")

# read the data from the file
irg_rough = pd.read_csv(example_file, header=[0,1], na_values='NAN')

start_time = irg_rough['TIMESTAMP'].values[0][0]
end_time = irg_rough["TIMESTAMP"].values[len(irg_rough["TIMESTAMP"].values)-1][0]

irg_rough['TIMESTAMP'] = irg_rough['TIMESTAMP'].astype(str)
irg_rough['TIMESTAMP']= pd.to_datetime(irg_rough['TIMESTAMP'].stack(),format='%Y-%m-%d %H:%M:%S').unstack()

irg_rough = irg_rough.set_index(pd.DatetimeIndex(irg_rough['TIMESTAMP'].values[:].flatten()))




d0 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
d1= datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
secSteps = 60*60
dt = datetime.timedelta(seconds = secSteps)
dates = np.arange(d0, d1, dt).astype(datetime.datetime)



heat_flux = []
date_lst = []
air_temp = []
vertical_vel = [] 
water_flux = []
ws_lst = []
wdir_lst = []
u_vel_lst = []
v_vel_lst = []
for i in range(0,len(dates)-1):
    act_df = irg_rough.loc[np.datetime64(dates[i]):np.datetime64(dates[i+1])]
    #perturb_Ts = act_df['Ts'].values.flatten() - np.nanmean(act_df['Ts'].values.flatten())
    #perturb_W = act_df['Uz'].values.flatten() - np.nanmean(act_df['Uz'].values.flatten())
    
    c = np.cov(act_df['Ts'].values.flatten(),act_df['Uz'].values.flatten())
    d = np.cov(act_df['H2O'].values.flatten(),act_df['Uz'].values.flatten())
    #air_temp.append(np.nanmean(act_df['Ts'].values.flatten()))
    
    u_vel = np.nanmean(act_df['Ux'].values.flatten())
    v_vel = np.nanmean(act_df['Uy'].values.flatten()) 
    ws = calcwindspeed(v_vel,u_vel)
    wdir = calcwinddirection(u_vel,v_vel)
    
    
    
    vertical_vel.append(np.nanmean(act_df['Uz'].values.flatten()))
    air_temp.append(np.nanmean(act_df['Ts'].values.flatten()))
    
    u_vel_lst.append(u_vel)
    v_vel_lst.append(v_vel)
    ws_lst.append(ws)
    wdir_lst.append(wdir)
    heat_flux.append(c[0,1])
    water_flux.append(d[0,1])
    date_lst.append(np.datetime64(dates[i])+ np.timedelta64(12,'h') + + np.timedelta64(5,'m'))


avg = pd.DataFrame({'TIMESTAMP': date_lst, 'Tair':air_temp, 'u':u_vel_lst, 'v':v_vel_lst, 'w':vertical_vel, 'WS':ws_lst, 'WD':wdir_lst,  'cov_TsW':heat_flux, 'cov_H2OW':water_flux})


avg.to_csv(wd_path+"/smooth_60min_avg.csv")




plt.plot(heat_flux)
plt.plot(u_vel_lst)




heatflux_rough.plot(x='TIMESTAMP',y='cov_H2OW', linewidth=1)


heatflux_rough.plot(x='TIMESTAMP',y='cov_TsW', linewidth=1)
plt.ylim(-0.5, 0.5)


fig = heatflux_rough.plot(x='TIMESTAMP',y='cov_H2OW', linewidth=1).get_figure() 
plt.ylim(-0.25, 0.25)
fig.savefig(wd_path+'rough_cov_H2OW15.jpg', bbox_inches='tight', dpi=600)



fig = heatflux_rough.plot(x='TIMESTAMP',y='W', linewidth=1).get_figure()
     
fig.savefig(wd_path+'smooth_W15.jpg', bbox_inches='tight', dpi=600)





fig = heatflux_rough.plot(x='TIMESTAMP',y='W', linewidth=1).get_figure()  
#heatflux_rough.plot.line(x='TIMESTAMP', y='W')
plt.ylim(-2, 15) 
fig.savefig(wd_path+'rough_TW.jpg', bbox_inches='tight', dpi=600)


heatflux_rough.plot(x='TIMESTAMP',y='Ts\'W\'', linewidth=1)
instant_heat_flux = np.array(instant_heat_flux).flatten()
plt.plot(heatflux_rough['cov_TsW'])      
plt.plot(instant_heat_flux)    
plt.ylim(-0.25, 0.25) 
        


fig = heatflux_rough.plot(x='TIMESTAMP',y='cov_TsW', linewidth=1).get_figure()
plt.ylim(-0.5, 0.5)     
fig.savefig(wd_path+'rough_covTsW.jpg', bbox_inches='tight', dpi=600)
    
        
        
        
        
        
        
        
        
        
        
        
        
        