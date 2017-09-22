# -*- coding: utf-8 -*-
from pandas import Series,DataFrame

#from PCI_trans import eci2cgi

import pandas as pd

cdfg = pd.read_csv('C:\Work\JXWLJG\\09_21\MRO-CDFG-20170921-all.csv',encoding = 'utf-8')
del cdfg['\t']

cdfg2 = cdfg[['CGI.1','重叠覆盖点数','大于-110采样点数']].dropna().groupby('CGI.1',as_index=False).sum()

cdfg2['重叠覆盖度']=cdfg2['重叠覆盖点数']/cdfg2['大于-110采样点数']

#cdfg2['cgi']=cdfg2['eci'].map(lambda x:"460-00-" + str(int(hex(x)[2:7],16)) + "-" + str(int(hex(x)[-2:],16)))

base1 = pd.read_csv('C:\Work\JXWLJG\\0618gc_wg.csv', encoding = 'utf-8')

cdfg2 = pd.merge(cdfg2,base1.loc[:,['CGI','小区中文名','本地小区标识','覆盖类型','网格','地市','区县','覆盖场景','厂家名称','经\
度','纬度','工作频段']],left_on = 'CGI.1',right_on = 'CGI',how ='left')

cdfg2.to_csv('C:\Work\JXWLJG\\09_21\\0921_counts_new2.csv',encoding = 'utf-8')