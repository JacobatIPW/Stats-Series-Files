# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 07:06:11 2019

@author: Jacob
"""

import csv
i = 0
data_list = []
with open('usa_00003.csv', newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        i+=1
        data_list.append(row)
        if i > 30000:
            break

#Range
justIncome = []
for row in data_list[1:]:
    if int(row[6]) != 9999999:
        justIncome.append(int(row[6]))
        
minIncome = min(justIncome)
maxIncome = max(justIncome)
calRange= maxIncome - minIncome
print('The range is ', calRange, ' and goes from ', minIncome, ' to ', maxIncome)


#Interquartile Range
sortedData = []
for row in data_list[1:]:
    if int(row[6]) != 9999999:
        sortedData.append(int(row[6]))
sortedData.sort()
sampleSize = len(sortedData)
q1 = sampleSize*0.25
q2 = sampleSize*0.50
q3 = sampleSize*0.75
median = sortedData[round(q2)]
q1Income = sortedData[round(q1)]
q3Income = sortedData[round(q3)]
iqr = q3Income - q1Income
print('Interquartile Range: ', iqr)
print('Median: ', median)
print('25th percentile: ', q1Income)
print('75th percentile: ', q3Income)


#Variance
#Start with the average mean
totalSumIncome = 0
for row in sortedData:
    totalSumIncome = row + totalSumIncome
mean = totalSumIncome/sampleSize
print('Mean: ', mean)
sumOfSquares = 0
for row in sortedData:
    deviationScore = row - mean
    sumOfSquares = (deviationScore*deviationScore)+sumOfSquares
print('Sum of Squares: ', sumOfSquares)   
variance = sumOfSquares/(sampleSize-1)
print('Variance: ', variance)
import math
SD = math.sqrt(variance)
print("Standard Deviation: ", SD)


kurtosis = mean/SD
print('kurtosis: ', kurtosis)























































        
        
        
        
        
        