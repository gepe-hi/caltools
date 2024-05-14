#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads calibration files from EK80 (XMLs) given in path (and its subfolder)
Todo:
    Read calibration hits
    
@author: gp
"""

import glob
import pandas as pd
import xml.etree.ElementTree as ET

# Path to folder structure with all calibration XMLs
# A script has first been run to copy files from ces
# vessel='GOSARS'
vesselName='KRISTINEBONNEVIE'
# vesselName='PRINSESSEINGRIDALEXANDRA'
# vesselName='KRONPRINSHAAKON'
# path = r'/mnt/e/Calibration/'+vesselName+'/**/*.xml'
path = r'/mnt/d/Calibration/'+vesselName+'/**/*.xml'
files = glob.glob(path, recursive=True)

# Test files:
# files=['/mnt/f/CRIMAC/Calibration/2024/S2024001001_PGOSARS_4174/CalibrationDataFile-D20240105-T121517.xml',
        # '/mnt/f/CRIMAC/Calibration/2023/S2023001016_PGOSARS_4174/CalibrationDataFile-D20231116-T222320-FM-120-381.xml']

# Fields to use from XML-files
listFields=['Calibration/Common/Transducer',
            # 'Calibration/TargetReference',
            'Calibration/CalibrationResults',
            'Calibration/Common',
            'Calibration/Common/EnvironmentData']
            #'Calibration/TargetHits/HitData']

# Loop over files
for count, _count in enumerate(files):
    count
    tree = ET.parse(files[count])
    root = tree.getroot()

    # Loop over fields
    for field, _fields in enumerate(listFields):
        # There is a lot of junk in the folders, skip XMLs which does not have
        # calibration results. Files are written out in the display.
        try:
            # Read element
            def extract_data_custom(root, element_name):
                data = []
                for record in root.findall(f'.//{element_name}'):
                    row = {}
                    for field in record:
                        row[field.tag] = field.text
                    data.append(row)
                return data
            # Convert to dataframe
            def to_dataframe(data):
                df = pd.DataFrame(data)
                return df
        
            data = extract_data_custom(root, listFields[field])
         
            # Stupid part which likely has a much better solution
            # Initiation of dataframe
            if listFields[field]== listFields[0]:
                df = to_dataframe(data)
            else:
                dftemp = to_dataframe(data)
                df = pd.concat([df,dftemp],axis=1)
            
            # Add Mode / FM or CW based on length of Frequency field    
            if listFields[field]== listFields[1]:
                if len(data[0]['Frequency'])>6:
                        df.insert(0, "Mode", ['FM'], True)
                else:
                        df.insert(0, "Mode", ['CW'], True)
        except:
            print(files[count] + ' did not contain CalibrationResults')

    # Stupid part which likely has a much better solution
    # (we're concatinating dataframes here an not adding dicts.)
    if count == 0:
        dg = df
    else:
        dg = pd.concat([dg,df])


dg.reset_index(inplace=True)

# Convert relevant objects to float
convert_dict={'SerialNumber': float,
              #'NominalTransducerFrequency': float,
              'Temperature': float,
              'Salinity': float,
              'SoundVelocity': float,
              'AbsorptionCoefficient': float,
              'Acidity': float}

dg = dg.astype(convert_dict)

# Split relevant objects
dg['Gain']=dg['Gain'].str.split(';')
dg['Frequency']=dg['Frequency'].str.split(';')
dg['BeamWidthAlongship']=dg['BeamWidthAlongship'].str.split(';')
dg['BeamWidthAthwartship']=dg['BeamWidthAthwartship'].str.split(';')
dg['AngleOffsetAlongship']=dg['AngleOffsetAlongship'].str.split(';')
dg['AngleOffsetAthwartship']=dg['AngleOffsetAthwartship'].str.split(';')
dg['TsRmsError']=dg['TsRmsError'].str.split(';')

# Explode the above objects and convert to float
dg=dg.explode(['Gain', 'Frequency','BeamWidthAlongship','BeamWidthAthwartship',
               'AngleOffsetAlongship','AngleOffsetAthwartship','TsRmsError'])

convert_dict={'Gain': float,
              'Frequency': float,
              'BeamWidthAlongship': float,
              'BeamWidthAthwartship': float,
              'AngleOffsetAlongship': float,
              'AngleOffsetAthwartship': float,
              'TsRmsError': float}

dg = dg.astype(convert_dict)

del dg['index']

dg.to_pickle('../data/calibration'+vesselName+'.pkl')