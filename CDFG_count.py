# -*- coding: utf-8 -*-
from pandas import Series,DataFrame
from PCI_trans import eci2cgi
import pandas as pd

cdfg = pd.read_csv('C:\Work\JXWLJG\MR_07_222324\MRO-CDFG-20170723-all.csv',encoding = 'utf-8')
del cdfg['\t']

cdfg2 = cdfg[['CGI.1','重叠覆盖点数','大于-110采样点数']].dropna().groupby('CGI.1',as_index=False).sum()

cdfg2['重叠覆盖度']=cdfg2['重叠覆盖点数']/cdfg2['大于-110采样点数']

base1 = pd.read_csv('061C:\Work\JXWLJGgc.csv',encoding = 'utf-8')

result = pd.merge(cdfg2,base1.loc[:,['CGI','覆盖类型','网格','地市','区县']],left_on = 'cgi',right_on = 'CGI',how ='left')