# -*- coding: utf-8 -*-
from pandas import Series,DataFrame
<<<<<<< HEAD
from PCI_trans import eci2cgi
=======
#from PCI_trans import eci2cgi
>>>>>>> e11b8fc68964f664b66d9d942608065cfddf3df1
import pandas as pd

cdfg = pd.read_csv('C:\data\MRO-CDFG-20170730-all.csv',encoding = 'utf-8')
del cdfg['\t']

cdfg2 = cdfg[['CGI.1','重叠覆盖点数','大于-110采样点数']].dropna().groupby('CGI.1',as_index=False).sum()

cdfg2['重叠覆盖度']=cdfg2['重叠覆盖点数']/cdfg2['大于-110采样点数']

<<<<<<< HEAD
base1 = pd.read_csv('061C:\Work\JXWLJGgc.csv',encoding = 'utf-8')

result = pd.merge(cdfg2,base1.loc[:,['CGI','覆盖类型','网格','地市','区县']],left_on = 'cgi',right_on = 'CGI',how ='left')
=======
#cdfg2['cgi']=cdfg2['eci'].map(lambda x:"460-00-" + str(int(hex(x)[2:7],16)) + "-" + str(int(hex(x)[-2:],16)))

base1 = pd.read_csv('C:\data\\0618gc.csv', encoding = 'utf-8')

cdfg2 = pd.merge(cdfg2,base1.loc[:,['CGI','覆盖类型','网格','地市','区县','覆盖场景','厂家名称','经度','纬度','工作频段',]],left_on = 'CGI.1',right_on = 'CGI',how ='left')

>>>>>>> e11b8fc68964f664b66d9d942608065cfddf3df1
