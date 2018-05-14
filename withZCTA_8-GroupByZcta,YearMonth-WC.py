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
fileName = "withZCTA_8 DOB Permit Issuance" #change name of file to what it should be
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
zctaCol = 1 #set column where date data is 
dateCol = 4 #set column where data to be counted/summed is

for col in cols:
    if col[zctaCol] == 0 or col[zctaCol] == "":
        skipCount += 1
        continue
    
    try:
        month,day,year = col[dateCol].split('/')
    except ValueError:
        skipCount += 1
        continue
    month = str(month).zfill(2)
    year = year.rsplit(" ")
    year = int(year[0])
    '''
    if (year < 1998 or year > 2018) is True:
        skipCount += 1
        continue
    '''
    ym = str(year) + "-" + str(month)
    zcta = str(col[zctaCol])
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
for d in data.keys():
    for m in list(data[d].keys()):
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