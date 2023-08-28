#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Check system that Jupyter is running on # results --> file path

#import sys
#sys.executable

# Run in terminal -- To check if pandas is installed in the same environment as Jupyter Notebook
#/opt/homebrew/opt/python@3.8/bin/python3.8 -m pip list | grep pandas 

# also numpy and matplotlib, any other packages 

# Run in terminal if packages not installed using:
#/opt/homebrew/opt/python@3.8/bin/python3.8 -m pip install pandas numpy matplotlib

# Run in terminal if pylib not installed using:
#/opt/homebrew/opt/python@3.8/bin/python3.8 -m pip install git+https://github.com/wzhengui/pylibs.git

#### If this fails, try again? Failed on first attempt then succeeded when tried again


# In[2]:


# import needed packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylib import *

### Pandas for data manipulation, NumPy for numerical computations, and Matplotlib for data visualization.
### Pylib for all three, plus more useful tools


# In[3]:


########################### Salinity Dataset ##################################

# Pandas read_csv automatically reads into a dataframe 
salt_data = pd.read_csv('/Users/kboothomefolder/phy577_projects/data/LaJolla_data/LaJolla_SALT_1916-202303.csv', skiprows=0)

#print(salt_data[0:5])
#print(salt_data.iloc[:,0:5])

# Define variables for timeseries
# Since we skipped the first row when looking at the csv file, we do NOT need to reassign any of the variables because they default to float. 
# NaN is already used for these datasets so no need to replace
# Observations collected daily for the full timeframe

# convert to numpy array (problem in Jupyter)

SSal, BSal = np.asarray(salt_data.loc[:,'SURF_SAL_PSU']), np.asarray(salt_data.loc[:,'BOT_SAL_PSU'])
salt_data['datestr']=salt_data.iloc[:,0:3].astype(str).apply('-'.join,axis=1)

# use pandas to convert datestr column to a format recognizable by pandas
time=np.asarray(pd.to_datetime(salt_data.datestr,format='%Y-%m-%d'))

############ Subplots ###################

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot SSal on the first subplot
ax1.scatter(time, SSal, color='blue', label='SSal', s=5)
ax1.set_ylabel('Surface Salinity (PSU)')
ax1.legend()

# Plot BSal on the second subplot
ax2.scatter(time, BSal, color='green', label='SSal', s=5)
ax2.set_xlabel('Time (year)')
ax2.set_ylabel('Bottom Salinity (PSU)')
ax2.legend()

plt.suptitle('Surface and Bottom Salinity Time Series')
#plt.show()

#savefig('/Users/kboothomefolder/phy577_projects/hw1/figures/Sal_LJ.png')

# Save the figures

output_dir = '/Users/kboothomefolder/phy577_projects/hw1/figures'
savefig(os.path.join(output_dir, 'LJ_salinity.png'))


# In[ ]:


# Plot time-series of Salinity  - same plot
### Plot includes NaN values as empty spaces, default  of Matplotlib when plotting dataframes with NaNs.
#plot(time, SSal, 'r', label='Surface Salinity')
#plot(time, BSal, 'b', label='Bottom Salinity')
#grid(True)
#ylabel('Salinity (PSU)')
#xlabel('Time')
#title('Surface and Bottom Salinity - La Jolla')
#savefig('/Users/kboothomefolder/phy577_projects/hw1/figures/Sal_LJ.png')
#close() # close figure to start on next


# In[ ]:


############################# Temperature Dataset #############################3

temp_data = pd.read_csv('/Users/kboothomefolder/phy577_projects/data/LaJolla_data/LaJolla_TEMP_1916-202303.csv', skiprows=0)
STemp, BTemp = np.asarray(temp_data.loc[:,'SURF_TEMP_C']), np.asarray(temp_data.loc[:,'BOT_TEMP_C'])
temp_data['datestr']=temp_data.iloc[:,0:3].astype(str).apply('-'.join,axis=1)
time=np.asarray(pd.to_datetime(temp_data.datestr,format='%Y-%m-%d'))

#plot(time, STemp, 'r', label='Surface Temperature')
#plot(time, BTemp, 'b', label='Bottom Temperature')
#grid(True)
#ylabel('Temperature (C)')
#xlabel('Time')
#title('Surface and Bottom Temperature -  La Jolla')
#savefig('/Users/kboothomefolder/phy577_projects/hw1/figures/Temp_LJ.png')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
#ax1.plot(time, STemp, color='blue', label='STemp')
ax1.scatter(time, STemp, color='blue', label='STemp', s=5)
ax1.set_ylabel('Surface Temperature (C)')
ax1.legend()
ax2.scatter(time, BTemp, color='green', label='BTemp', s=5)
#ax2.plot(time, BTemp, color='green', label='BTemp')
ax2.set_xlabel('Time (year)')
ax2.set_ylabel('Bottom Temperature (C)')
ax2.legend()
plt.suptitle('Surface and Bottom Temperature Time Series')
#plt.show()

#savefig('/Users/kboothomefolder/phy577_projects/hw1/figures/Temp_LJ.png')

#output_dir = '/Users/kboothomefolder/phy577_projects/hw1/figures'
savefig(os.path.join(output_dir, 'LJ_temp.png'))


# In[ ]:




