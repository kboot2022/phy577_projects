from pylib import *

S=loadz('PS_WQ_2021.npz')
mod=loadz('/home/bootk/Analysis/RUN02a/mod_at_ps_wq_stations.npz')

####### make a plot of all 9 stations --- Temperature

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')

xts,xls=xts[::90],xls[::90]; xls[0]=xls[0]+''

for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.temp[pd], label='In-Situ')
    plot(mod.time+datenum(2019,1,1)+8/24,mod.temp[i,:], label='Model')
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    #plt.title('PS {}'.format(i))
    plt.tight_layout()
    plt.legend(loc="best")
    title('PS {}'.format(i+1))


show(block=False)
savefig('TempStationsAll_Comp_PS_RUN02a.png')

####### make a plot of all 19 stations (11 are operational) --- Salinity

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')

xts,xls=xts[::90],xls[::90]; xls[0]=xls[0]+''

for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.salt[pd], label='In-Situ')
    plot(mod.time+datenum(2019,1,1)+8/24,mod.salt[i,:], label='Model')
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    #plt.title('PS {}'.format(i))
    plt.tight_layout()
    plt.legend(loc="best")
    title('PS {}'.format(i+1))

show(block=False)
savefig('SaltStationsAll_Comp_PS_RUN01d.png')

##############################################
#####Basic Plot Configuration

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')
xts,xls=xts[::30],xls[::30]; xls[0]=xls[0]+', 2018'

stas=arange(0,190,10)

##### Plot the specific stations

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

S=loadz('NRE_WQ_2019.npz')
mod=loadz('/home/bootk/Analysis/APS/Obs/ModMon/mod_at_nre_wq_stations.npz')
##### Poster plots - stations, 50, 100, 140, 180 Salinity
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

##### Poster plots - stations, 50, 100, 140, 180 Temperature

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



