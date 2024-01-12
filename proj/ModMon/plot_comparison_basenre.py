from pylib import *

S=loadz('NRE_WQ_2019.npz')
mod=loadz('/home/bootk/Analysis/RUN02a_qq/mod_at_nre_stations.npz')

####### make a plot of all 19 stations (11 are operational)--- Salinity

## Stations 0, 20, 30, 50, 60, 70, 100, 120, 140, 160, and 180 (11 total) have observations in the NRE_WQ_2019.npz dataset. 

## Stations 10, 40, 80, 90, 110, 130, 150, and 170 do NOT have observations in the dataset. 

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')

xts,xls=xts[::90],xls[::90]; xls[0]=xls[0]+''

stas=arange(0,190,10)
flag=0
for i in [0, 2, 3, 5, 6, 7, 10, 12, 14, 16, 18]:
    flag=flag+1
    print(i)
    subplot(3,4,flag)
    pd=(S.station==i*10)*(S.depthcat=='S')
    plot(mod.time+datenum(2019,1,1)+8/24,mod.salt[i,:], label='Model')
    plot(S.time[pd],S.salt[pd], label='In-Situ')
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    plt.title('NRE {}'.format(i*10))
    plt.tight_layout()
    if flag == 1: plt.legend(loc="best")

show(block=False)

savefig('SaltStationsAll_Comp_NRE_RUN02a.png')
