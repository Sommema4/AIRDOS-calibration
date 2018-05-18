# # Spectrum Interactive
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas import DataFrame
import string
import os
import matplotlib.pyplot as plt
import matplotlib
import optparse

'''
Creates .csv file with the energy spectra from the selected time interval.
Uses the ginput function which allows you to choose interval of interest by clicking at two points in figure.
Takes one parameter - name of the datalog file from AIRDOS
Variable csvName should be stated
'''
csvName = 'Am241.csv'

# Parse option
parser = optparse.OptionParser()
parser.add_option('-f', '--file', dest='file', help='File name')
(options, args) = parser.parse_args()

l=[]
l.extend(range(0,520))
df = pd.read_table(options.file, sep=',', header=None, names=l, comment='*',engine='python')

df.drop(df[df[0]=='$GPTXT'].index, inplace=True)
#df.drop(r[r[0]=='$GPRMC'].index, inplace=True)
df.drop(df[df[0]=='$GPVTG'].index, inplace=True)
df.drop(df[df[0]=='$GPGLL'].index, inplace=True)
df.drop(df[df[0]=='$GPGSA'].index, inplace=True)
df.drop(df[df[0]=='$GPGSV'].index, inplace=True)
#df.drop(df[df[0]=='$CANDY'].index, inplace=True)

matplotlib.rcParams.update({'font.size': 20})

rc = df.loc[df[0]=='$CANDY']
rc.reset_index(drop=True, inplace=True)

rc = rc.apply(pd.to_numeric, errors='coerce')

rc['sum'] = rc[range(270,513)].sum(axis=1)

#plt.figure(figsize=(20,5))
plt.yscale('log')

rc.ix[:,'sum'].plot(c='black')

plt.title('Select 10 points.')
plt.xlabel('Measurement No.')
plt.ylabel('Flux [counts per 10 s]')

#----------- Select Measurements in Flux diagram -----------------------------
points=plt.ginput(10)

e1 = [points[0][0],points[1][0]]

rc.ix[e1[0]:e1[1],'sum'].plot(c='blue')

plt.title('AIRDOS')
plt.xlabel('measurement No.')
plt.ylabel('Flux [counts per 10 s]')

#----------- Plot Spectrum -----------------------------
LOW_ENERGY = 256

ener1 = rc.ix[e1[0]:e1[1],LOW_ENERGY:513].sum()

# ## Save Histogram Data
ener1.to_csv(csvName)

ener1 = pd.read_table(csvName, sep=',', header=None, comment='*',engine='python')

plt.figure(figsize=(15,10))
plt.yscale('log')

#ener1.plot( label='e1')
plt.plot(ener1[0],ener1[1], label='e1', drawstyle='steps-pre', c='blue')

#plt.ylim([0,20000])
#plt.xlim([600,750])
plt.legend()
plt.title('AIRDOS Spectrum')
plt.xlabel('Channel')
plt.ylabel('Counts')
#plt.xticks(range(500,1030,10))
plt.xticks(rotation=90)
plt.grid()
