# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 12:11:50 2019

@author: Jacob
"""

import csv
import random
import matplotlib.pyplot as plt

incomeData = []

with open('usa_00003.csv', newline = '') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) >1:
                if int(row[6]) != 9999999:
                    if int(row[1]) > 17:
                        incomeData.append(int(row[6]))

def getSample(population, sampleSize):
    sampleList = random.sample(population, sampleSize)
    return sampleList

#Sample Mean
def getMean(sampleList):
    sampleSize = len(sampleList)
    totalSumIncome = 0
    for row in sampleList:
        totalSumIncome = row + totalSumIncome
    mean = totalSumIncome/sampleSize
    return mean

#Skew and Kurtosis
def getSkewAndKurtosis(sampleList):
    sampleSize = len(sampleList)
    #Mean again
    totalSumIncome = 0
    for row in sampleList:
        totalSumIncome = row + totalSumIncome
    mean = totalSumIncome/sampleSize
    #Variance
    sumOfSquares = 0
    s3 = 0
    s4 = 0
    for row in sampleList:
        deviationScore = row - mean
        sumOfSquares = deviationScore**2 + sumOfSquares
        s3 = deviationScore**3 + s3
        s4 = deviationScore**4 + s4
    variance = sumOfSquares/(sampleSize - 1)
    #Standard deviation 
    SD = variance**0.5
    #kurtosis
    n = sampleSize
    s2 = sumOfSquares
    sampleKurtosis = ((n*(n+1))/((n-1)*(n-2)*(n-3)))*((n-1)**2)*(s4/(s2**2))
    #Skew
    sampleSkew = s3/((n-1)*SD**3)
    return sampleSkew, sampleKurtosis
    
x = 0
n = 1000 #Sample size
statsOfSamples = []
numOfSamples = 3000
while x < numOfSamples:
    x+=1
    mySample = getSample(incomeData,n)
    mySampleMean = getMean(mySample)
    statsOfSamples.append(mySampleMean)
popMean = getMean(incomeData)
meanOfMeans = getMean(statsOfSamples)
skew, kurtosis = getSkewAndKurtosis(statsOfSamples)
popSkew, popKurtosis = getSkewAndKurtosis(incomeData)

print('Population Mean: ', popMean)
print('Mean of Means: ', meanOfMeans)
print('Skew: ', skew)
print('Kurtosis: ', kurtosis)
print('Population Kurtosis: ', popKurtosis)
print('Population Skew: ', popSkew)

plt.hist(statsOfSamples, bins = 50)
plt.show()
















  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        