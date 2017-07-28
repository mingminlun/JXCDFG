# -*- coding: utf-8 -*-
from pandas import Series,DataFrame
import pandas as pd

cdfg = pd.read_csv('C:\Work\JXWLJG\MR_07_222324\MRO-CDFG-20170723-all.csv',encoding = 'utf-8')
del cdfg['\t']

cdfg2 = cdfg[['CGI.1','重叠覆盖点数','大于-110采样点数']].dropna()

grouped = cdfg2.groupby('CGI.1',as_index=False)


