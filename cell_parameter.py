import csv
from collections import namedtuple

file = open('C:\Work\JXWLJG\\0928gc.csv', encoding='UTF-8')


def cpTrans(f):
    cell = namedtuple('cell', ['city', 'county', 'pci', 'earfcn', 'cgi', 'type', 'lon', 'lat', 'etilt', 'mtilt', 'tilt',
                               'azimuth', 'height'])
    cells = {}
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for line in f_csv:
        temp_line = cell(line[2], line[3], line[8], line[10], line[11], line[13], line[17], line[18], line[23],
                         line[24], line[26], line[26], line[27])
        cells[line[11]] = temp_line
    return cells


def cpExtract(f, city=None, county=None):#输出cgi,pci,earfcn,lon,lat,azimuth
    cells = []
    f_csv = csv.reader(f)
    next(f_csv)
    if (city is None) and (county is None):
        for line in f_csv:
            if line[17] != '' and line[18] != '':
                cells.append([line[11], line[8], line[10], line[17], line[18],line[26]])
    elif (city is not None) and (county is None):
        for line in f_csv:
            if line[2] == city and line[17] != '' and line[18] != '':
                cells.append([line[11], line[8], line[10], line[17], line[18],line[26]])
    elif (city is None) and (county is not None):
        for line in f_csv:
            if line[3] == county and line[17] != '' and line[18] != '':
                cells.append([line[11], line[8], line[10], line[17], line[18],line[26]])
    else:
        for line in f_csv:
            if (line[2] == city) and (line[3] == county) and line[17] != '' and line[18] != '':
                cells.append([line[11], line[8], line[10], line[17], line[18],line[26]])
    return cells
