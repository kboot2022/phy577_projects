#!/usr/bin/env python3
from pylib import *

#-----------------------------------------------------
#download NOAA elevation data:  NAVD and MSL
#-----------------------------------------------------
#read data

# coordinates of PS stations (nre10 to nre180)
lon_nre=c_[-77.12220, -77.0904, -77.0765, -77.0353, -77.0317, -77.0064, -76.9693, -76.9594, -76.9442, -76.9215, -76.8755, -76.8418, -76.81515, -76.7678, -76.7374, -76.6977, -76.66407, -76.5972, -76.52602 ]
lat_nre=c_[35.21060, 35.17793, 35.15330, 35.11375, 35.10972, 35.07952, 35.02465, 35.01472, 34.99860, 34.99050, 34.97660, 34.96170, 34.94888, 34.9525, 34.96610, 34.98750, 35.0144, 35.0274, 35.06413]
stas=arange(0,190,10)

mtime=[]; station=[]; elev=[]; depthcat=[];depth=[]; temp=[]; salt=[]; do=[]; ph=[];lon=[];lat=[]
fid=open('NREWQ_9Nov2021.csv','r'); lines=fid.readlines(); fid.close(); lines=lines[1:]
lines=lines[8725:-1] # only look at data after year 2010. Not sure about station names for data before 2010

for i in arange(len(lines)):
    display(i)
    line=lines[i].split(',')
    if len(line[3])>3: continue;
    if line[0] =='': break
    if line[6][0]=='-': continue;
    doyi=datestr2num(line[0]+' '+ line[6]); 
    sta=float(line[3]);depc=line[5]; dep=float(line[7]); tempi=float(line[8]); salti=float(line[10]);
   
#Test station numbers coordinated with lat/lon entries before defining lati/loni elements   
    #salti=float(line[10]);
    ind=(stas==sta)
    loni=lon_nre[0,ind]; lati=lat_nre[0,ind]

    #save record
    mtime.append(doyi)
    station.append(sta)
    depthcat.append(depc)
    lon.append(loni)
    lat.append(lati)
    depth.append(dep)
    temp.append(tempi)
    salt.append(salti)




#-save data-------
S=npz_data(); S.time=array(mtime); S.lon=array(lon); S.lat=array(lat); S.depthcat=array(depthcat);S.depth=array(depth)
S.temp=array(temp); S.salt=array(salt); S.do=array(do); S.ph=array(ph)
S.station=array(station).astype('int')


# add lat&lon information
#Lat=dict(zip(C.station,C.lat)); Lon=dict(zip(C.station,C.lon))
#S.lat=array([Lat[i] for i in S.station])
#S.lon=array([Lon[i] for i in S.station])
save_npz('NRE_WQ_2019',S)


S=loadz('NRE_WQ_2019.npz')
mod=loadz('/home/bootk/Analysis/APS/Obs/ModMon/mod_at_nre_wq_stations.npz')

# make a sample plot
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')
xts,xls=xts[::30],xls[::30]; xls[0]=xls[0]+', 2018'

stas=arange(0,190,10)

for i in arange(19):
    print(i)
    subplot(5,5,i+1)
    pd=(S.station==stas[i])*(S.depthcat=='S') # changed to S.depth from S.depthcat b/c data difference
    plot(S.time[pd],S.temp[pd])
    plot(mod.time+datenum(2019,1,1)+8/24,mod.temp[i,:])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,31)],ylim=[0,30])
    title('{}'.format(i+1))

    #title('NRE WQ Sampling station {}'.format(i+1))

show(block=False)
savefig('Temperature_NRE_WQ.png')

flag=0
for i in [5, 10, 14, 18]:
    flag=flag+1
    print(i)
    subplot(2,2,flag)
    pd=(S.station==i*10)*(S.depthcat=='S')
    plot(mod.time+datenum(2019,1,1)+8/24,mod.salt[i,:])
    plot(S.time[pd],S.salt[pd])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('{}'.format(i*10))
    #title('NRE WQ Sampling station {}'.format(i+1))


show(block=False)
savefig('Salt_NRE_WQ.png')

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::30],xls[::30]; xls[0]=xls[0]+', 2018'

for i in arange(19):
    print(i)
    subplot(5,5,i+1)
    pd=(S.station==i+1)*(S.depthcat=='S')
    plot(S.time[pd],S.salt[pd])
    plot(mod.time+datenum(2019,1,1)+8/24,mod.salt[i,:])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('{}'.format(i+1))

#Poster plots - stations 50, 100, 140, and 180 salt and temp 
show(block=False)

S=loadz('NRE_WQ_2019.npz')
mod=loadz('/home/bootk/Analysis/APS/Obs/ModMon/mod_at_nre_wq_stations.npz')

#Figure Dimensions and labelling
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')
xts,xls=xts[::90],xls[::90]; xls[0]=xls[0]+''

stas=arange(0,190,10)

flag=0
for i in [5, 10, 14, 18]:
    flag=flag+1
    print(i)
    subplot(2,2,flag)
    pd=(S.station==i*10)*(S.depthcat=='S')
    plot(mod.time+datenum(2019,1,1)+8/24,mod.salt[i,:])
    plot(S.time[pd],S.salt[pd])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,25])
    title('Station {}'.format(i*10))
    plt.suptitle('ModMon Station Data Comparison with 2019 Model Run Output', fontsize = 20)
    plt.ylabel("Salinity (PSU)")
    plt.tight_layout()

show(block=False)
savefig('SaltStations_NRE_WQ.png')

# Make a plot for temperature comparison

flag=0
for i in [5, 10, 14, 18]:
    flag=flag+1
    print(i)
    subplot(2,2,flag)
    pd=(S.station==i*10)*(S.depthcat=='S')
    plot(mod.time+datenum(2019,1,1)+8/24,mod.temp[i,:])
    plot(S.time[pd],S.temp[pd])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('Station {}'.format(i*10))
    plt.ylabel("Temperature ($^\circ$C)")
    plt.tight_layout()
    if flag == 1: plt.legend(loc="best")

show(block=False)
savefig('TempStations_NRE_WQ.png')
