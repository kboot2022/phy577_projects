#!/usr/bin/env python3
from pylib import *

#-----------------------------------------------------
#download NOAA elevation data:  NAVD and MSL
#-----------------------------------------------------
#read data

mtime=[]; cast=[]; elev=[]; depthcat=[];depth=[]; temp=[]; salt=[]; do=[]; ph=[];lon=[];lat=[]
fid=open('Pamlico_Sound_FerryMon_2019.csv','r'); lines=fid.readlines(); fid.close(); lines=lines[3:]

for i in arange(len(lines)):
    display(i)
    line=lines[i].split(',')
    #if len(line[3])>3: continue;
    #if line[0] =='': break
    #if line[6][0]=='-': continue;
    doyi=datestr2num(line[0][0]); 
    castno=float(line[1]); dep=float(line[8]); tempi=float(line[4])
    loni=float(line[14]);lati=float(line[13]);
    salti=float(line[6]);

#Test station numbers coordinated with lat/lon entries before defining lati/loni elements   

    #save record
    mtime.append(doyi)
    cast.append(castno)
    lon.append(loni)
    lat.append(lati)
    depth.append(dep)
    temp.append(tempi)
    salt.append(salti)




#-save data-------
S=npz_data(); S.time=array(mtime); S.lon=array(lon); S.lat=array(lat);S.depth=array(depth)
S.temp=array(temp); S.salt=array(salt);
S.cast=array(cast).astype('int')


# add lat&lon information
#Lat=dict(zip(C.station,C.lat)); Lon=dict(zip(C.station,C.lon))
#S.lat=array([Lat[i] for i in S.station])
#S.lon=array([Lon[i] for i in S.station])
save_npz('NRE_FM_WQ_2019',S)


S=loadz('NRE_FM_WQ_2019.npz')
mod=loadz('/home/bootk/Analysis/APS/RUN01/ModMon_test2.npz')

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
mod=loadz('/home/bootk/Analysis/APS/RUN01/ModMon_test2.npz')

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

show(block=False)
savefig('TempStations_NRE_WQ.png')
