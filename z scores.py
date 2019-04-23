# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 16:28:40 2019

@author: Jacob
"""

import csv

incomeData = []
with open('usa_00003.csv', newline = '') as myFile:
    data = csv.reader(myFile)
    for row in data:
        #Skip the header
        if row[6] != 'INCTOT':
            #Skip anyone who did not earn or had a negative income
            if int(row[6]) > 1:
                #Skip NA
                if int(row[6]) != 9999999:
                    #Skip anyone under the age of 18
                    if int(row[1]) > 17:
                        incomeData.append(int(row[6]))
                        
#Function for mean
def getMean(sampleList):
    sampleSize = len(sampleList)
    totalSumIncome = 0
    for row in sampleList:
        totalSumIncome = totalSumIncome + row
    mean = totalSumIncome/sampleSize
    return mean
    
#Function to get population Standard Deviation
def getPopSD(sampleList, mean):
    sumOfSquares = 0
    sampleSize = len(sampleList)
    for row in sampleList:
        deviationScore = row - mean
        sumOfSquares = deviationScore**2+sumOfSquares
    #               Rather than sampleSize - 1 like in sample SD
    variance = sumOfSquares/sampleSize
    SD = variance**0.5
    return SD
    
mean = getMean(incomeData)
popSD = getPopSD(incomeData, mean)

#Select some income
z = 168000
#Calculate the z score for that income
z_score = (z-mean)/popSD
z_score = round(z_score,2)
print('This is the z score: ', z_score)

#Load in our z table from earlier
z_table = []
with open('z_table.csv', newline='') as zTableFile:
    data = csv.reader(zTableFile)
    for row in data:
        z_table.append(row)
        
#Find the percentile rank of our z score in the z table
for row in z_table:
    if float(row[0]) == z_score:
        probability = row[1]
        percentile = round(float(probability)*100,2)
        print('An income of ',z,'has a standard score of',z_score,
              'which corresponds to a percentile of',percentile)
        break























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

                        
                        
                        
                        
                        
                        
                        
                        
                        