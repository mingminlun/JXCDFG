from pandas import Series,DataFrame
import pandas as pd

df1 = pd.read_csv('result.csv',encoding = 'utf-8')
df1.columns=['0','sc_cgi','sc_name','samples','nc_cgi','nc_name']
del df1['0']

