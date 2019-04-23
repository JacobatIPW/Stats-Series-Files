# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 13:44:05 2019

@author: Jacob
"""

import csv
i = 0
incomeData = []
with open('usa_00003.csv', newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        i+=1
        if row[6] != 'INCTOT':
            if int(row[6]) > 1:
                if int(row[6]) != 9999999:
                    incomeData.append(int(row[6]))
        if i > 30000:
            break

        
#Sample Size
sampleSize = len(incomeData)
print('Sample Size: ', sampleSize)    

#Sample Mean
totalSumIncome = 0
for row in incomeData:
    totalSumIncome = row + totalSumIncome
mean = totalSumIncome/sampleSize
print('Mean: ', mean)

#Variance
sumOfSquares = 0
s3 = 0
s4 = 0

for row in incomeData:
    deviationScore = row - mean
    sumOfSquares = deviationScore**2 + sumOfSquares
    s3 = deviationScore**3 + s3
    s4 = deviationScore**4 + s4
variance = sumOfSquares/(sampleSize - 1)
print('Variance: ', variance)

#Standard Deviation
SD = variance**0.5
print('Standard Deviantion: ', SD)

#Kurtosis
n = sampleSize
s2 = sumOfSquares
m2 = s2/n
m4 = s4/n
populationKurtosis = (m4/m2**2)-3
print('Population Kurtosis: ', populationKurtosis)
sampleKurtosis  = (((n*(n+1))/((n-1)*(n-2)*(n-3)))*((n-1)**2)*(s4/(s2**2)))-3
print('Sample Kurtosis: ', sampleKurtosis)

#Skewness
sampleSkew = s3/((n-1)*SD**3)
print('Sample Skewness: ', sampleSkew)

#Check our Work
import pandas as pd
df = pd.DataFrame({'INCTOT':incomeData})
testKurtosis = pd.Series.kurtosis(df)
print('Test Kurtosis: ', testKurtosis)
testSkew = df.skew()
print('Test Skew: ', testSkew)




















































        
        
        
        
        
        
        
        
        
        
        
        
