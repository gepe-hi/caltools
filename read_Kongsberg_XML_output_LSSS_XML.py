#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:37:25 2024
Read a KD calibration XML file (results) and create LSSS calibration.xml
Prior knowledge is needed to include calibration for each LSSS channel, and
to assign the appropriate channel to each calibration result.
@author: gp
"""

import pandas as pd
import xml.etree.ElementTree as ET
import glob
import numpy as np

# Assumed prior knowledge, needs to be read first (NilsOlav has code for that)
# Dummy data based on 'TrList_calibration_CW_FM2msFast.xml'
f0 = np.concatenate([np.ones(4) * 38000, np.ones(4) * 70000, np.ones(4) * 120000, np.ones(4) * 200000, np.ones(4) * 333000])
transducer = np.array(['ES38-7', 'ES38-7', 'ES38-7', 'ES38-7', 'ES70-7CD','ES70-7CD','ES70-7CD','ES70-7CD','ES120-7CD','ES120-7CD','ES120-7CD','ES120-7CD','ES200-7CD','ES200-7CD','ES200-7CD','ES200-7CD','ES333-7CD','ES333-7CD','ES333-7CD','ES333-7CD'])
mode = np.array(['CW', 'CW', 'CW', 'FM','CW', 'CW', 'CW', 'FM','CW', 'CW', 'CW', 'FM','CW', 'CW', 'CW', 'FM','CW', 'CW', 'CW', 'FM'])
channels=np.arange(0,len(mode),1)+1
dt = pd.DataFrame({'Channel': channels, 'Frequency': f0, 'Type': mode, 'TransducerName': transducer})
print(dt)

# Parse XML file
path = r'/mnt/c/Users/a32685/Documents/Matlab/2024_CalSplit/TrList_calibration_CW_FM2msFast.xml'
out_path='/mnt/c/Users/a32685/Documents/Matlab/2024_CalSplit/EK80/calibration.xml'
files = glob.glob(path, recursive=True)
tree = ET.parse(files[0])
root = tree.getroot()

# Define lists to store data
data = {
    'TransducerName': [],
    'Type': [],
    'hz': [],
    'g': [],
    'SA': [],
    'albw': [],
    'atbw': [],
    'alao': [],
    'atao': [],
    'Impedance': [],
    'Phase': [],
    'PulseLength': [],
    'TransmitPower': [],
    'Case': []
}

# Loop through Transducer elements
for transducer in root.findall('./TransducerData/Transducer'):
    transducer_name = transducer.get('TransducerName')
    
    # Loop through FrequencyParCW elements
    for freq_cw in transducer.findall('./FrequencyParCW'):
        data['TransducerName'].append(transducer_name)
        data['Type'].append('CW')
        data['hz'].append((freq_cw.get('Frequency')))
        data['g'].append(float(freq_cw.get('Gain')))
        #data['SA'].append(float(freq_cw.get('SaCorrection')))
        data['SA'].append(str(int(float(freq_cw.get('PulseLength'))*1000*1000))+':'+str((float(freq_cw.get('SaCorrection')))))
        data['albw'].append(float(freq_cw.get('BeamWidthAlongship')))
        data['atbw'].append(float(freq_cw.get('BeamWidthAthwartship')))
        data['alao'].append(float(freq_cw.get('AngleOffsetAlongship')))
        data['atao'].append(float(freq_cw.get('AngleOffsetAthwartship')))
        data['Impedance'].append(float(freq_cw.get('Impedance')))
        data['Phase'].append(float(freq_cw.get('Phase')))
        data['PulseLength'].append(float(freq_cw.get('PulseLength')))
        data['TransmitPower'].append(int(freq_cw.get('TransmitPower')))
        data['Case'].append((freq_cw.get('RefNo')))
    
    # Loop through FrequencyPar elements
    for freq_par in transducer.findall('./FrequencyPar'):
        data['TransducerName'].append(transducer_name)
        data['Type'].append('FM')
        data['hz'].append((freq_par.get('Frequency')))
        data['g'].append(float(freq_par.get('Gain')))
        data['SA'].append(float(freq_par.get('SaCorrection')))
        data['albw'].append(float(freq_par.get('BeamWidthAlongship')))
        data['atbw'].append(float(freq_par.get('BeamWidthAthwartship')))
        data['alao'].append(float(freq_par.get('AngleOffsetAlongship')))
        data['atao'].append(float(freq_par.get('AngleOffsetAthwartship')))
        data['Impedance'].append(float(freq_par.get('Impedance')))
        data['Phase'].append(float(freq_par.get('Phase')))
        data['PulseLength'].append(None)
        data['TransmitPower'].append(None)
        data['Case'].append((freq_par.get('RefNo')))

# Create DataFrame
df = pd.DataFrame(data)

# Expand dataframe so that each channel has its own calibration. Assign correct channel to each
length=np.arange(0,len(channels),1)
for ind in length:
    if ind==0:
        tmp=df.loc[(df['TransducerName']==((dt['TransducerName'][ind]))) & (df['Type']==((dt['Type'][ind])))]
        tmp['Case']=dt['Channel'][ind]
        dq=pd.DataFrame()
        dq=pd.concat([dq,tmp])
        # dq.append(tmp)
    elif ind>0:    
        tmp=df.loc[(df['TransducerName']==((dt['TransducerName'][ind]))) & (df['Type']==((dt['Type'][ind])))]
        tmp['Case']=dt['Channel'][ind]
        dq=pd.concat([dq,tmp])
    
df=dq

# Write the XML file

cases = ((pd.unique(df.Case)))
length=np.arange(0,len(df.Case),1)

xml_out=open(out_path,'wb')
xml_out.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'utf-8'))
xml_out.write(bytes('<calibration>\n', 'utf-8'))

for ind in cases:
    da=df.loc[df['Case']==ind]
    da=da.reset_index(col_level=0)
    print(da)
    if da.Type[0]=='CW':
        str1='<case channel="' + str(da.Case[0]) + '" khz="' + str(int(float(da.hz[0])/1000))
        str2='" g="' + str(da.g[0]) +'" SA="' + da.SA[0] +'"/>\n'
        str12=str1+str2
        xml_out.write(bytes(str12, 'utf-8'))
    if da.Type[0]=='FM':
        fmlen=len(da)
        print(fmlen)
        str1='<case channel="' + str(da.Case[0]) +'">\n'
        xml_out.write(bytes(str1, 'utf-8'))
        str1='        <broadband>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        str1='        <g>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        count=np.arange(0,fmlen)
        for indg in count:
            str1='        <case hz="' + da.hz[indg] + '" g="' + str(da.g[indg]) + '"/>\n'
            xml_out.write(bytes(str1, 'utf-8'))
        str1='        </g>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        # eba
        str1='        <albw>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        for indg in count:
            str1='        <case hz="' + da.hz[indg] + '" albw="' + str(da.albw[indg]) + '"/>\n'
            xml_out.write(bytes(str1, 'utf-8'))
        str1='        </albw>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        # Athwartship width
        str1='        <atbw>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        for indg in count:
            str1='        <case hz="' + da.hz[indg] + '" atbw="' + str(da.atbw[indg]) + '"/>\n'
            xml_out.write(bytes(str1, 'utf-8'))
        str1='        </atbw>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        # Alongship offset
        str1='        <alao>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        for indg in count:
            str1='        <case hz="' + da.hz[indg] + '" alao="' + str(da.alao[indg]) + '"/>\n'
            xml_out.write(bytes(str1, 'utf-8'))
        str1='        </alao>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        # Athwartship offset
        str1='        <atao>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        for indg in count:
            str1='        <case hz="' + da.hz[indg] + '" atao="' + str(da.atao[indg]) + '"/>\n'
            xml_out.write(bytes(str1, 'utf-8'))
        str1='        </atao>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        # Close broadband case
        str1='        </broadband>\n'
        xml_out.write(bytes(str1, 'utf-8'))
        str1='        </case>\n'
        xml_out.write(bytes(str1, 'utf-8'))

xml_out.write(bytes('</calibration>', 'utf-8'))

xml_out.close()
