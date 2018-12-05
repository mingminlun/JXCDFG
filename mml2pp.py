import sys
import re

mml_array = ['LST CELL:;','LST RRU:;','DSP CELLPHYTOPO:;']

with open('test_data.txt',encoding='utf-8',errors='ignore') as f:
    # lines = f.readlines()
    try:
        while True:
            line = next(f)
            line.strip()
            if line != "":
                if included_in_array(line,mml_array)[0] == 1:
                    nodeb_name = next(f).replace('网元 : ','').strip()


                elif '+++' in line:
            

                
    except StopIteration:
        pass

'''
for line in lines:
    line.strip()
    if line != "":
        if included_in_array(arr,array)[0] == 1:
'''            
        

def included_in_str(str1,array):#检测指令数组内的指令是否和语句相同
    for arr in array:
        flag = 0
        if arr == str1 or ("命令-----" + arr) == str1:
            return 1,arr
        else:
            flag = flag + 1
    if flag == 3:
        return 0,None





