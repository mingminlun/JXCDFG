import csv

rows = []

eci2cgi = lambda x: "460-00-" + str(int(hex(x)[2:7], 16)) + "-" + str(int(hex(x)[-2:], 16))

with open('C:\Work\JXWLJG\\11_02\MRO-CDFGPCI-20171102-all',encoding='UTF-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    sc_eci = None
    sc_cgi = None
    line = []
    for row in f_csv:
        if row[0] != sc_eci:
            rows.append(line)
            line = []
            sc_eci = row[0]
            sc_cgi = eci2cgi(int(sc_eci))
            line = [sc_cgi]
            line.append(row[5])
        else:
            line.append(row[5])
    rows.append(line)

with open('C:\Work\JXWLJG\\11_02\change.csv','w') as r:
    r_csv = csv.writer(r,lineterminator='\n')
    r_csv.writerows(rows)


