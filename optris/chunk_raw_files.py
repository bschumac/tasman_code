#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 17:31:01 2020

@author: benjamin

Chunking of 1 GB .raw files from OPTRIS Camera 
"""


import os
import shutil
datapath = "/mnt/Seagate_Drive1/TAS2/raw_TAS2/"
fls = os.listdir(datapath)

start = "w."
#end = ".raw"
#Sorting files:
fls = sorted(fls, key = lambda x: float(x[x.rfind(start)+len(start):len(x)]))






for i in range(0,len(fls),20):
    print(i)
    # create directories
    os.makedirs(datapath+str(i//20))
    
    try:
        for j in range(i,i+20):
            # rename files and move into correct folders
            if j == 0:
                
                original_name = fls[j]
                newname = original_name[:-2]
                print(datapath+str(i//20)+"/"+newname)
                #shutil.move(datapath+fls[0], datapath+str(i//20)+"/"+newname)
            elif j == i:
                original_name = fls[j]
                rep = int(original_name[original_name.rfind(start)+len(start):len(original_name)])
                dig = len(str(rep))
                last_char_index = original_name.rfind("."+str(rep))
                newname = original_name[:last_char_index] + "" + original_name[last_char_index+1+dig:]
                shutil.move(datapath+fls[j-1], datapath+str(i//20)+"/"+newname)
                print(datapath+str(i//20)+"/"+newname)
            elif j == len(fls):
                pass
            else:
                original_name = fls[j]
                rep = int(original_name[original_name.rfind(start)+len(start):len(original_name)])
                dig = len(str(rep))
                last_char_index = original_name.rfind(str(rep))
                newname = original_name[:last_char_index] + original_name[last_char_index+dig:] + str(j-i+1)
                print(datapath+str(i//20)+"/"+newname)
                #print()
                shutil.move(datapath+fls[j-1], datapath+str(i//20)+"/"+newname)
                
    except:
        pass
        
            
        
        

new_string = original_string[:last_char_index] + "" + original_string[last_char_index+dig:]
