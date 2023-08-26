# Manually downloaded data from https://library.ucsd.edu/dc/object/bb4003017c due to some difficulty with zipfile format

import pandas as pd
import matplotlib.pyplot as plt
from pylib import *
########################### Salinity Dataset ##################################

salt_data = pd.read_csv('/Users/kboothomefolder/phy577_projects/data/LaJolla_data/LaJolla_SALT_1916-202303.csv', skiprows=0)

print(salt_data[0:5])

# drop first row because it's titles
#salt_data = salt_data.drop([0])

# Define variables for timeseries
SSal = salt_data.loc[:,'SURF_SAL_PSU']
BSal = salt_data.loc[:,'BOT_SAL_PSU']

# Since we skipped the first row when looking at the csv file, we do NOT need #to reassign any of the variables because they default to float. 

# NaN is already used for these datasets so no need to replace

# It seems like values are collected daily for the full timeframe

print(salt_data.iloc[:,0:5])
salt_data['datestr']=salt_data.iloc[:,0:3].astype(str).apply('-'.join,axis=1)

# use pandas to convert datestr column to a format recognizable by pandas

time=pd.to_datetime(salt_data.datestr,format='%Y-%m-%d')
print(time)

plot(time, SSal, 'r', label='Surface Salinity')
plot(time, BSal, 'b', label='Bottom Salinity')
grid(True)
ylabel('Salinity (PSU)')
xlabel('Time')
title('Surface and Bottom Salinity - La Jolla')
savefig('/Users/kboothomefolder/phy577_projects/hw1/figures/Sal_LJ.png')
close()

############################# Temperature Dataset #############################3

temp_data = pd.read_csv('/Users/kboothomefolder/phy577_projects/data/LaJolla_data/LaJolla_TEMP_1916-202303.csv', skiprows=0)

#print(temp_data.iloc[:,5:])

# drop first row because it's titles
#temp_data = temp_data.drop([0])

# Define variables for timeseries
STemp = temp_data.loc[:,'SURF_TEMP_C']
BTemp = temp_data.loc[:,'BOT_TEMP_C']

# Since we skipped the first row when looking at the csv file, we do NOT need
#to reassign any of the variables because they default to float.

# NaN is already used for these datasets so no need to replace

# It seems like values are collected daily for the full timeframe

#print(temp_data.iloc[:,0:5])
temp_data['datestr']=temp_data.iloc[:,0:3].astype(str).apply('-'.join,axis=1)

# use pandas to convert datestr column to a format recognizable by pandas

time=pd.to_datetime(temp_data.datestr,format='%Y-%m-%d')
#print(time)

plot(time, STemp, 'r', label='Surface Temperature')
plot(time, BTemp, 'b', label='Bottom Temperature')
grid(True)
ylabel('Temperature (C)')
xlabel('Time')
title('Surface and Bottom Temperature -  La Jolla')
savefig('/Users/kboothomefolder/phy577_projects/hw1/figures/Temp_LJ.png')
