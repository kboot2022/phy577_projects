#!/usr/bin/env python3
from pylib import *

#-----------------------------------------------------
#download NOAA elevation data:  NAVD and MSL
#-----------------------------------------------------
#read data

# coordinates of PS stations (ps1 to ps9)
lon_ps=c_[-76.47653, -76.42758,-76.34330,-76.26680,-76.20060,-76.24867,-76.22947,-76.30570,-76.37275]
lat_ps=c_[35.1201,35.15056667,35.13125,35.11841667,35.1225,35.08255,35.03205,35.02616667,35.09986667]

mtime=[]; station=[]; elev=[]; depthcat=[];depth=[]; temp=[]; salt=[]; do=[]; ph=[];lon=[];lat=[]
fid=open('/home/bootk/Analysis/APS/Obs2021/Obs/ModMon/PS_WQ_2021_WQData.csv','r'); lines=fid.readlines(); fid.close(); lines=lines[1:]
lines=lines[302:-1] # only look at data after year 2001. Not sure about station names for data before 2001

for i in arange(len(lines)):
    line=lines[i].split(',')
    if line[0] =='': break
    doyi=datestr2num(line[0]); sta=float(line[2]);depc=int(line[3]); dep=float(line[5]); tempi=float(line[6])
    salti=float(line[8]); dox=float(line[9]); phi=float(line[10])
    loni=lon_ps[0,int(sta)-1]; lati=lat_ps[0,int(sta)-1]

    #save record
    mtime.append(doyi)
    station.append(sta)
    depthcat.append(depc)
    lon.append(loni)
    lat.append(lati)
    depth.append(dep)
    temp.append(tempi)
    salt.append(salti)
    do.append(dox)
    ph.append(phi)




#-save data-------
S=npz_data(); S.time=array(mtime); S.lon=array(lon); S.lat=array(lat); S.depthcat=array(depthcat);S.depth=array(depth)
S.temp=array(temp); S.salt=array(salt); S.do=array(do); S.ph=array(ph)
S.station=array(station).astype('int')


# add lat&lon information
#Lat=dict(zip(C.station,C.lat)); Lon=dict(zip(C.station,C.lon))
#S.lat=array([Lat[i] for i in S.station])
#S.lon=array([Lon[i] for i in S.station])
save_npz('PS_WQ_2021',S)


S=loadz('PS_WQ_2021.npz')
mod=loadz('../../RUN01/mod_at_ps_wq_stations.npz')

# make a sample plot
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::30],xls[::30]; xls[0]=xls[0]+', 2018'

for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.temp[pd])
    plot(mod.time+datenum(2019,1,1)+8/24,mod.temp[i,:])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('PS WQ Sampling station {}'.format(i+1))


show(block=False)
savefig('Temperature_PS_WQ.png')

for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.salt[pd])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('PS WQ Sampling station {}'.format(i+1))


show(block=False)
savefig('Salt_PS_WQ.png')

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::30],xls[::30]; xls[0]=xls[0]+', 2018'

for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.salt[pd])
    plot(mod.time+datenum(2019,1,1)+8/24,mod.salt[i,:])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('PS WQ Sampling station {}'.format(i+1))


show(block=False)


