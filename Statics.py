from pandas import DataFrame
import pandas as pd

cdfg = pd.read_csv('C:\Work\JXWLJG\\11_02\MRO-CDFG-20171102-all.csv',encoding = 'utf-8')
nc = pd.read_csv('C:\Work\JXWLJG\\11_02\change.csv',encoding = 'utf-8')
phr = pd.read_csv('C:\Work\JXWLJG\\11_02\MRS-PowerHeadRoom-20171102-all.csv',encoding = 'utf-8')

del cdfg['\t']
del phr['\t']

stastics = pd.merge(nc,cdfg,left_on = 'cgi',right_on = 'CGI.1',how = 'left')
stastics = pd.merge(stastics,phr,left_on = 'cgi',right_on = 'CGI',how = 'left')