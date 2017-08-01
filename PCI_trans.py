# -*- coding: utf-8 -*-
from pandas import Series,DataFrame
import pandas as pd
import math

idx = pd.IndexSlice

df1 = pd.read_csv('C:\data\\7_27a',skiprows = 1,names =['eci','sc_ear','nc_ear','nc_pci','t','6dB'])
del df1['t']

base1 = pd.read_csv('C:\data\\0618gc.csv',encoding = 'utf-8')

r = 6371229

#dis = lambda lng1,lat1,lng2,lat2:math.sqrt(((lng1-lng2)*math.pi*r*math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)**2+((lat1 - lat2)*math.pi*r/180)**2)

ear_trans = lambda ear:ear+2640 if (ear >= 37750 and ear<=38249) else ear
 
eci2cgi = lambda x:"460-00-" + str(int(hex(x)[2:7],16)) + "-" + str(int(hex(x)[-2:],16))

df1['cgi']=df1['eci'].map(lambda x:"460-00-" + str(int(hex(x)[2:7],16)) + "-" + str(int(hex(x)[-2:],16)))

df1 = pd.merge(df1,base1.loc[:,['CGI','覆盖类型','网格','地市','区县']],left_on = 'cgi',right_on = 'CGI',how ='left')

df1 = df1.set_index(['覆盖类型','网格']).sortlevel(0).dropna()
df1 = df1.ix['室外'].ix['网格内'].reset_index()

df1['sc_ear']=df1['sc_ear'].apply(ear_trans)
df1['nc_ear']=df1['nc_ear'].apply(ear_trans)
base1['中心载频的信道号']=base1['中心载频的信道号'].apply(ear_trans)

base2= base1.set_index(['覆盖类型','物理小区识别码','中心载频的信道号','地市','区县','CGI'],drop=False).sortlevel(0).drop(['室内'],axis = 0)

result = DataFrame()

def dis2(row):
    return math.sqrt(((row['经度']-row['sc_lng'])*math.pi*r*math.cos(((row['纬度'] + row['sc_lat']) / 2) * math.pi / 180) / 180)**2 + ((row['纬度'] - row['sc_lat'])*math.pi*r/180) **2)

CGI = list(base2['CGI'])

for ix, row in df1.iterrows():
# ix = 18684

    sc_cgi = str(df1.loc[ix,'cgi'])
    nc_earfcn = df1.loc[ix,'nc_ear']
    nc_pci = df1.loc[ix,'nc_pci']
    samples = df1.loc[ix,'6dB']
    
    if sc_cgi in CGI:
        sc_name = list(base2.loc[idx[:,:,:,:,:,sc_cgi],idx['小区中文名']])[0]
        sc_city = list(base2.loc[idx[:,:,:,:,:,sc_cgi],idx['地市']])[0]
        sc_county = list(base2.loc[idx[:,:,:,:,:,sc_cgi],idx['区县']])[0]
        sc_lng = float(base2.loc[idx[:,:,:,:,:,sc_cgi],idx['经度']])
        sc_lat = float(base2.loc[idx[:,:,:,:,:,sc_cgi],idx['纬度']])
        
        tempdf = base2.loc[idx[:,nc_pci,nc_earfcn,sc_city,sc_county,:],idx['经度','纬度']]
        if tempdf.empty != True:
            tempdf['sc_lng']= sc_lng
            tempdf['sc_lat']= sc_lat
            tempdf['dis'] = tempdf.apply(dis2,axis=1)
            min_cell =tempdf['dis'].idxmin(axis =1)
            
            if type(min_cell) == tuple:
                nc_cgi = min_cell[5]
                nc_name = list(base2.loc[idx[:,:,:,:,:,nc_cgi],idx['小区中文名']])[0]
        
                row = DataFrame([sc_cgi,sc_name,samples,nc_cgi,nc_name]).T
        
                result =result.append(row)
                
                print(ix)


                
#a =base2.loc[idx[:,:,:,:,'460-00-934049-138'],idx['经度']] 
#a =base2.loc[idx[:,:,:,:,df1.loc[0,'cgi']],idx['经度']]
#base2.loc[idx[:,nc_pci,nc_earfcn,sc_city,sc_county,:],idx['经度','纬度']]选取待比较小区
#def dis2(lng1,lat1):
#   return lambda lng1,lat1,lng2,lat2:math.sqrt(((lng1-lng2)*math.pi*r*math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)**2+((lat1 - lat2)*math.pi*r/180)**2)
#base2.loc[:,['经度','纬度']]type