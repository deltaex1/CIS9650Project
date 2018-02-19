#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 15:24:28 2018

@author: Wilson
"""

filename = ""

while filename != "exit": #sentinel value to break program, all within program must follow 1 indent
    filename = input("Enter the name of the file (without the .csv extension) to analyze (or enter 'exit' to exit): ")
    if filename == "exit":
        print("Thank you for using this tool! bye bye :-)")
        break #need break statement
    
    file = open(filename + ".csv")
    
    print("\n" + "Reading Data..." + "\n")
    lines = file.readlines()
    file.close()

    amountearned = {}
    amountspent = {}
    txnCount= {}
    
    trucks = ["A","B"]
    validtxn = ["earned","spent"]
    
    for line in lines:
        col = line.split(",")
        truck = str(col[0])
        earnspent = str(col[1])
        amount = float(col[2])
        
        if truck not in trucks or earnspent not in validtxn: #checks for invalid values condition Level 1
            if truck not in trucks: #checks for specific invalid values and  then handling
                print("Found Error in Data: Invalid truck: " + str(truck))
                continue #skips iteration
            
            elif earnspent not in validtxn: 
                print("Found Error in Data: Invalid earned/spent data: " + earnspent)
                continue #skips iteration
              
        if earnspent == "earned":
            if truck in txnCount: #counts # of transaction for average calculation
                txnCount[truck] += 1
            else:
                txnCount[truck] = 1#assumes valid values, devises condition to handle
            
            if truck in amountearned: #Reference must be to the entire dictionary key, NOT a specific value e.g. amountearned[truck]
                amountearned[truck] += amount
            else:
                amountearned[truck] = amount
                
        elif earnspent == "spent":
            if truck in amountspent:
                amountspent[truck] += amount
            else:
                amountspent[truck] = amount
    
    print("\n" + "Done reading the data, Starting analysis..." + "\n") #MUST INDENT PROPERLY, within first WHILE loop

#Loop truck keys to display sums and calculations
    for truck in trucks: #NOT part of line loading loop
        print("On truck " + str(truck) + ", we spent $" + str(amountspent[truck]))
        print("On truck " + str(truck) + ", we earned $" + str(amountearned[truck]))
        print("On truck " + str(truck) + ", we made a profit of $" + str((amountearned[truck] - amountspent[truck])))
        print("On truck " + str(truck) + ", average earned amount is $" + str(amountearned[truck]/txnCount[truck]))
        print("\n")

#Display final sum of totals        
    print("In total, we spent $" + str(sum(amountspent.values())))
    print("In total, we earned $" + str(sum(amountearned.values())))
    print("In total, we made a profit of $" + 
        str(float(sum(amountearned.values()) - float(sum(amountspent.values())))))
        #Math operation of dictionary requires formatting as Float and not dict
