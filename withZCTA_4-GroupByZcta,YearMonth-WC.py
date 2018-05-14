#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 10:41:12 2018

@modified by: Wilson
"""

import csv
#import pandas as pd
#import collections
# import numpy as np
#fileName = input("File name:") # user gives me a file name
fileName = "withZCTA_4 Restaurrant_DOHMH_Food_Permits (1)"
f = open(fileName + ".csv", "r") # add .csv extension and open file
cols = csv.reader(f)

header = []
header = next(cols)

day = 0
month = 0
year = 0
data = {}
skipCount = 0
runCount = 0

for col in cols:
    if col[4] == 0 or col[1] == "":
        skipCount += 1
        continue
    
    try:
        month,day,year = col[4].split('/')
    except ValueError:
        skipCount += 1
        continue
    month = str(month).zfill(2)
    year = year.rsplit(" ")
    year = int(year[0])
    
    if (year < 1998 or year > 2018) is True:
        skipCount += 1
        continue
    
    ym = str(year) + "-" + str(month)
    zcta = str(col[1])
    if zcta in data:
        if ym in data[zcta]:
            data[zcta][ym] += 1       
        else: data[zcta][ym] = 1
    else:
        data[zcta] = {}
        data[zcta][ym] = 1
        
    runCount += 1

writecount = 0
keyerror = 0
w = open(fileName + '-Processed.csv','w')
w.write('ZCTA,Year-Month,ZCTAcount\n')
for d in data:
    for m in data[d]:
        try:
            string = (str(d) +',' + str(m) + ',' + str(data[d][m]) + '\n')
        except KeyError:
            keyerror += 1
            continue
        w.write(string)
        writecount += 1
w.close()
print(str(runCount) + ' records proessed and ' + str(skipCount) + ' records skipped.')
print(str(keyerror) + ' keyErrors skipped and ' + str(writecount) + ' records written to ' + fileName + '.csv')