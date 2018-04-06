# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 21:44:35 2018

@author: Wilson
"""

import csv
#import urllib

class MedianRent:
    zipcode = ""
    year = 0
    month = 0
    mrent = 0.0
    sizerank = 0
    

fileLst = ["",
           "Zip_MedianListingPrice_AllHomes",
           "Zip_MedianListingPricePerSqft_AllHomes",
           "Zip_MedianListingPricePerSqft_Sfr",
            "Zip_MedianRentalPrice_AllHomes",
            "Zip_MedianRentalPricePerSqft_AllHomes",
            "Zip_MedianValuePerSqft_AllHomes",
            "Zip_PriceToRentRatio_AllHomes"]

for x in range(1, len(fileLst)):
    print(str(x) + " - " + str(fileLst[x]))
fs = int(input("Enter numeric choice: "))
#url = "http://files.zillowstatic.com/research/public/Zip/" + str(fileLst[fs]) + ".csv"
fname = fileLst[fs]
'''
fname = "Zip_MedianRentalPrice_AllHomes" 
fs = 0 #manual setting for coloffset
    '''
#print(url)
#f = urllib.request.urlopen(url)

f = open(fname+".csv")

#rows = csv.DictReader(f)
#cols = csv.reader(f.read().decode('utf-8'))
cols = csv.reader(f)

headerdata = []
headerdata = next(cols)
#print(headerdata)

data = []
ziplist = []

coloffset = 0 #adjust offset for columns depending on file
if fs > 5:
    coloffset = 1
else: coloffset = 0

next(cols)
for col in cols:
    
    if col[1 + coloffset] != "New York": #City = New York
        continue
    
    if col[0 + coloffset] not in ziplist: #unique zip list
        ziplist.append(col[0 + coloffset])
    
    for i in range((6 + coloffset), len(col)): #lower bound range is column offset where value starts
        if col[i] == "":
            continue
        else:
            r = MedianRent()
            r.zipcode = str(col[0 + coloffset])
            r.year, r.month = headerdata[i].split("-")
            r.mrent = float(col[i])
            r.sizerank = str(col[5 + coloffset])
            
            r.year = int(r.year)
            r.month = int(r.month)
            
            data.append(r)
        
writecount = 0
filename = 'RawData-' + fname +'.csv'
w = open(filename,'w')
w.write('zip,sizeRank,year,month,medianRent\n')
for r in data:
    string = (str(r.zipcode) +','+ str(r.sizerank) + ',' + str(r.year) +','+ str(r.month) \
               +','+ str(r.mrent) + "\n")
    w.write(string) #Give your csv text here.
    ## Python will convert \n to os.linesep
    writecount += 1
    
w.close()
print(str(writecount) + " lines of data written to " + str(filename))

writecount = 0
filename = 'Processed-' + fname + '.csv'
w = open(filename,'w')
w.write('ZipCode,Gradient,ObsCount,Max,Min,MaxYear,MinYear\n')

#GRADIENT CALCULATION
ziplist.sort()
import numpy

sYear = int(input("Enter starting year: "))
eYear = int(input("Enter ending year: "))

for s in ziplist:
    gradientLst = []
    valueLst = []
    zipFilter = list(filter(lambda r: (r.zipcode == s and r.year >= sYear and r.year <= eYear), data))
    for v in zipFilter:
        valueLst.append(v.mrent)
    valueLst = numpy.asarray(valueLst, dtype=float)
    gradientLst = numpy.gradient(valueLst)
    maxValue = max(zipFilter, key = lambda x: x.mrent)
    minValue = min(zipFilter, key = lambda x: x.mrent)
    maxYear = max(zipFilter, key = lambda x: x.year)
    minYear = min(zipFilter, key = lambda x: x.year)
    gradient = sum(gradientLst) / len(gradientLst)
    string = (str(s) + ',' + str(gradient) + ',' + str(len(gradientLst))
             + ',' + str(maxValue.mrent) + ',' + str(minValue.mrent) + ','
             + str(maxYear.year) + ',' + str(minYear.year) + "\n")
    w.write(string)
    writecount += 1
    '''
    print("Zip Code " + str(s) + " has a gradient of " + str(gradient) + " with " 
          + str(len(gradientLst)) + " observations, and Max of " + str(maxValue.mrent)
          + " and a Min of " + str(minValue.mrent) + " from " + str(minYear.year)
          + " to " + str(maxYear.year))   '''

w.close()
print(str(writecount) + " lines of data written to " + str(filename))

"""
#OPTIONAL GRAPHING COMPONENT FOR BASIC VISUALIZATION
ziplist.sort()
import matplotlib.pylab as plt

for x in ziplist:
    graphXaxis = []
    graphYaxis = []
    graphXlabels = []
    graphFilter = list(filter(lambda r: r.zipcode == x, data))
    i = 1
    for v in graphFilter:
        graphXaxis.append(i)
        graphXlabels.append(str(v.year + "-" + v.month))
        graphYaxis.append(v.mrent)
        i += 1
    plt.title(fname + " " + v.zipcode) #Graph title
    plt.plot(graphXaxis, graphYaxis) #graphs sequential X axis with correct Y values
    plt.xticks(graphXaxis, graphXlabels, rotation='vertical') #matches labels in correct axis order
    plt.xlabel("Year Month") #X axis label
    plt.ylabel("Median") #Y axis label
    plt.show()
"""