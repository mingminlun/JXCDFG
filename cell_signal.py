from math import sqrt, pi, cos
import csv


class Cell_signal():
    def __init__(self, cgi=None, earfcn=0, pci=0, rsrp=0, rsrq=0):
        self.cgi = cgi
        self.earfcn = earfcn
        self.pci = pci
        self.rsrp = rsrp
        self.rsrq = rsrq

    def __repr__(self):
        return 'cgi:%r,earfcn:%r,pci:%r,rsrp:%r,rsrq:%r' % (self.cgi, self.earfcn, self.pci, self.rsrp, self.rsrq)


def signal_high(cell_signal):
    return abs(int(cell_signal.rsrp))


class Samplepoint():
    def __init__(self, lon, lat, city, sc, nc):
        self.lon = lon
        self.lat = lat
        self.city = city
        self.sc = sc
        self.nc = nc

    def __repr__(self):
        return 'lon:%r,lat:%r,city:%r,sc:%r,nc:%r' % (self.lon, self.lat, self.city, self.sc, self.nc)


file = open('C:\Work\JXWLJG\\jaott.csv', encoding='UTF-8')


def sampleTrans(f):
    samplepts = []
    coordinate_set = []
    sampleScCgi = []
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        row_nc = row[9:row.index('\t')]
        temp_nc = []
        if row_nc[0] != 'NIL':
            for i in range(0, len(row_nc), 4):
                if row[5] == row_nc[i] and (int(row_nc[i + 2]) - int(row[7])) > -6:
                    temp_nc.append(Cell_signal(None, row_nc[i], row_nc[i + 1], row_nc[i + 2], row_nc[i + 3]))
            temp_nc.sort(key=signal_high)
        if len(temp_nc) >= 3:
            # if (int(temp_nc[2].rsrp) - int(row[7])) > -6:
            samplepts.append(
                Samplepoint(row[1], row[2], row[3], Cell_signal(row[4], row[5], row[6], row[7], row[8]), temp_nc))
            coordinate_set.append([float(row[1]), float(row[2])])
            sampleScCgi.append(row[4])
    return samplepts, coordinate_set,sampleScCgi


sample_list, coordinate_list = sampleTrans(file)


def outCsvTrans(sample_list):
    out_csv = []
    for sample in sample_list:
        out_line = [sample.lon, sample.lat, sample.city, sample.sc.cgi, sample.sc.earfcn, sample.sc.pci, sample.sc.rsrp,
                    sample.sc.rsrq]
        for nc in sample.nc:
            out_line += [nc.cgi, nc.earfcn, nc.pci, nc.rsrp, nc.rsrq]
        out_csv.append(out_line)
    return out_csv


'''
out_csv = outCsvTrans(sample_list)

with open('C:\Work\JXWLJG\\3ott1.csv', 'w') as r:
    r_csv = csv.writer(r, lineterminator='\n')
    r_csv.writerows(out_csv)
'''


def cgi_cal(samplepts, cellsCoor_with_cgi):
    for sample in samplepts:
        for nc in sample.nc:
            distances = []
            for line in cellsCoor_with_cgi:
                if nc.pci == line[1] and nc.earfcn == line[2]:
                    distances.append(
                        [distEclud(float(sample.lon), float(sample.lat), float(line[3]), float(line[4])),
                         line[0], line[1], line[2]])
            try:
                nc.cgi = sorted(distances)[0][1]
            except IndexError:
                print(nc)
    return samplepts


def distEclud(lonA, latA, lonB, latB):
    return sqrt(
        ((lonA - lonB) * pi * 6371229 * cos(((latA + latB) / 2) * pi / 180
                                            ) / 180) ** 2 + ((latA - latB) * pi * 6371229 / 180) ** 2)
