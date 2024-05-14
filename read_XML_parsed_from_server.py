#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A bit of playing around with the data

@author: gp
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import plotly.express as px

import plotly.io as io
io.renderers.default='browser'

# vesselName='KRISTINEBONNEVIE'
vesselName='GOSARS'
# vesselName='PRINSESSEINGRIDALEXANDRA'
# vesselName='KRONPRINSHAAKON'
df = pd.read_pickle('../data/calibration'+vesselName+'.pkl')

df.dtypes

dfg =  df.groupby(['Mode'])

# Plot all Gains

fig=px.scatter(df, x='Frequency',y='Gain', color='TimeOfFileCreation')
fig=px.scatter(df, x='Frequency',y='Gain', color='Temperature')
# fig=fig.add_trace(px.scatter(df,x='Frequency',y='Temperature'))
# fig=px.scatter(df,x='Frequency',y='Temperature')
fig.show()

# Plot Gains for CW at a particular frequency
freq=333
mode='CW'
a=df.loc[df.Mode == mode]
a=df.loc[df.Frequency == freq]
io.renderers.default='browser'
titleString=str(freq)+' kHz transducer - ' + mode
fig=px.scatter(a, x='TimeOfFileCreation',y='Gain',color='Temperature', title=titleString)
fig.show()

## Plot Gains for CW at a particular channel
mode='FM'
# transducer = 'ES18-11'
# transducer='ES38-7'
# transducer='ES70-7C'
# transducer='ES120-7C'
# transducer='ES200-7C'
transducer='ES333-7C'
b=df.loc[df.Mode == mode]
#b.plot(kind='scatter',x='Frequency', y='Gain')
# b=b.loc[b.Name == 'ES120-7C']
# b=b.loc[b.Name == 'ES333-7C']
b=b.loc[b.Name == transducer]
# io.renderers.default='svg'
b = b.sort_values(by="TimeOfFileCreation")
titleString=transducer + ' transducer - ' + mode
fig=px.scatter(b, x='Frequency',y='Gain',color='TimeOfFileCreation', title=titleString)
fig.show()

fig=px.scatter(b, x='Frequency',y='AngleOffsetAthwartship',color='TimeOfFileCreation', title=titleString)
fig.show()

fig=px.scatter(b, x='Frequency',y='AngleOffsetAlongship',color='TimeOfFileCreation', title=titleString)
fig.show()