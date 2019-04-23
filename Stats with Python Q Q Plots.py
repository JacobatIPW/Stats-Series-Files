# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 04:57:55 2019

@author: Jacob
"""

import csv

incomeData = []
with open('usa_00003.csv', newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) > 1:
                if int(row[6]) != 9999999:
                    if int(row[1]) > 17:
                        incomeData.append(int(row[6]))

#Get a sample
import random
sample = random.sample(incomeData,100)

sample.sort()
sampleSize = len(sample)

i = 1
sampleQuantiles = []
for row in sample:
    sampleQuantile = (i-0.5)/sampleSize
    i+=1
    sampleQuantiles.append(sampleQuantile)
    
z_table = []
with open('z_table.csv', newline = '') as zTableFile:
    data = csv.reader(zTableFile)
    for row in data:
        z_table.append(row)
        
z_scores_from_normal_distrobution = []
for row in sampleQuantiles:
    sample_quantile_probability = row
    i = 0
    for each in z_table:
        i+=1
        z_table_probability = each[1]
        #Values will not match exactly, so we need to find a close match
        if row <= float(each[1]):
            z_scores_from_normal_distrobution.append(each[0])
            break
        
def getMean(sampleList):
    sampleSize = len(sampleList)
    totalSum = 0
    for row in sampleList:
        totalSum = totalSum + row
        mean = totalSum/sampleSize
    return mean

def getSampleSD(sampleList, mean):
    sumOfSquares = 0
    sampleSize = len(sampleList)
    for row in sampleList:
        deviationScore = row - mean
        sumOfSquares = deviationScore**2+sumOfSquares
    variance = sumOfSquares/(sampleSize-1)
    SD = variance**0.5
    return SD
    
mean = getMean(sample)
SD = getSampleSD(sample,mean)

z_scores_actual = []
for row in sample:
    z_score = (row-mean)/SD
    z_scores_actual.append(z_score)
    

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

grey_patch = mpatches.Patch(color = 'grey', label='Expected Normal Quantiles')
black_patch = mpatches.Patch(color='black',label='Actual Quantiles')
plt.title('Normal Quantile-Quantile Plot')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.legend(handles=[grey_patch,black_patch])
plt.scatter(z_scores_from_normal_distrobution, z_scores_actual, color='black')
plt.scatter(z_scores_from_normal_distrobution,z_scores_from_normal_distrobution,
            color='grey')
plt.show()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        























                        