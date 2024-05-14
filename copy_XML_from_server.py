#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:37:52 2024

Script to copy calibration XMLs from CES/Cruise_data to a local folder structure

@author: gp
"""

import os
import shutil
import glob
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")

makeFolder = 1
year = list(range(2015, 2025))
# vesselName = 'GOSARS'
# vesselName='JOHANHJORT'
vesselName='KRISTINEBONNEVIE'
# vesselName='KRONPRINSHAAKON'
# vesselName='PRINSESSEINGRIDALEXANDRA'

vessel = '*'+vesselName+'*'
#rootFolder = '/mnt/z/tmp/test_Calibration/'+vesselName+'/'
#rootFolder = '/mnt/e/CALIBRATION/'+vesselName+'/'
rootFolder = '/mnt/d/CALIBRATION/'+vesselName+'/'

# The data is a mess on CES
# Just searching for XMLs under EK80_CALIBRATION
# They might be located in other directories, or there might be several 
# different calibrations in the same folder

cesRootFolder = '/mnt/w/'

for yr in year:
    dir_content = glob.glob(os.path.join(cesRootFolder, str(yr), vessel))
    
    for content in dir_content:
        tmp_path = os.path.join(content, 'ACOUSTIC','EK80')
        if not os.path.exists(tmp_path):
            tmp_path = os.path.join(content, 'ACOUSTIC_DATA','EK80')
        
        if not os.path.exists(tmp_path):
            continue    
        
        tmp = os.listdir(tmp_path)
        tmp
        
        for item in tmp:
            if item == 'EK80_CALIBRATION':
                tmp2_path = Path(tmp_path, 'EK80_CALIBRATION')
                tmp2 = list(tmp2_path.glob('**/*.xml'))
                
                if not os.path.exists(os.path.join(rootFolder, str(yr), content[12:-1])):
                    os.makedirs(os.path.join(rootFolder, str(yr), content[12:-1]))
                
                for file in tmp2:
                    findFileName=str(file)
                    fileName=findFileName.rpartition('/')[-1]
                    if os.path.isfile(os.path.join(rootFolder, str(yr), content[12:-1]+'/'+fileName)):
                        os.remove(os.path.join(rootFolder, str(yr), content[12:-1]+'/'+fileName))
                        # Sometimes, someone, used case sensitive folder names
                        # e.g. 70Khz and 70khz in the same folder
                    if os.path.isfile(str(file)):                            
                        shutil.copy(str(file), os.path.join(rootFolder, str(yr), content[12:-1]))
