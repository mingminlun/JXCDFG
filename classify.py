import cell_signal
import kmeans
from cell_parameter import cpExtract
import numpy as np
import csv


file = open('C:\Work\JXWLJG\\jaott.csv', encoding='UTF-8')

sample_list, coordinate_list,sampleScCgi_list = cell_signal.sampleTrans(file)

#centlist, clusterAssment = kmeans.biKmeans(np.mat(coordinate_list), 69)


'''
with open('C:\Work\JXWLJG\\centlist2.csv', 'w') as r:
    r_csv = csv.writer(r, lineterminator='\n')
    r_csv.writerows(centlist)

with open('C:\Work\JXWLJG\\clusterAssment2.csv', 'w') as r:
    r_csv = csv.writer(r, lineterminator='\n')
    r_csv.writerows(clusterAssment)
'''
cell_csv = open('C:\Work\JXWLJG\\0928gc.csv', encoding='UTF-8')

extractedCells = cpExtract(cell_csv, '吉安', '青原区')

samplepts = cell_signal.cgi_cal(sample_list,extractedCells)

out_csv = cell_signal.outCsvTrans(samplepts)

with open('C:\Work\JXWLJG\\3ott2.csv', 'w') as r:
    r_csv = csv.writer(r, lineterminator='\n')
    r_csv.writerows(out_csv)