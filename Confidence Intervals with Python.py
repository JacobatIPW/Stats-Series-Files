# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 17:05:42 2019

@author: Jacob
"""
import csv 

def getMean(sample):
    sumTotal = 0
    for row in sample:
        sumTotal += row
    sampleSize = len(sample)
    mean = sumTotal/sampleSize
    return mean
    
def getSampleSD(sample):
    mean = getMean(sample)
    sampleSize = len(sample)
    sumOfSquares = 0
    for row in sample:
        deviationScore = row - mean
        sumOfSquares = sumOfSquares + deviationScore**2
    variance = sumOfSquares/(sampleSize-1)
    sampleSD = variance**0.5
    return sampleSD
    
def getSampleStandardError(sample):
    sampleSD = getSampleSD(sample)
    sampleSize = len(sample)
    SEM = sampleSD/sampleSize**0.5
    return SEM
    
def getCriticalT(alpha, sample):
    sampleSize = len(sample)
    df = sampleSize - 1
    #different from last video
    if df > 120:
        df = 120
    criticalT = 0
    with open('t_table.csv', newline='') as tFile:
        tData = csv.reader(tFile)
        for row in tData:
            if int(row[0]) == df:
                if float(row[2]) >= (float(1-(alpha/2))):
                    criticalT = float(row[1])
                    break
    return criticalT
    
def getCI(sample, alpha):
    mean = getMean(sample)
    SEM = getSampleStandardError(sample)
    critT = getCriticalT(alpha, sample)
    lowerCI = mean - critT*SEM
    upperCI = mean + critT*SEM
    #different from last video
    error = critT*SEM
    return lowerCI, upperCI, error

#   0      1      2        3       4        5        6
#['SEX', 'AGE', 'RACE', 'RACED', 'EDUC', 'EDUCD', 'INCTOT']
#SEX - 1 male, 2 female
# Race - 1 white, 2 black, 3     
incomeDataMale = []
incomeDataFemale = []
with open('usa_00003.csv', newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) > 1:
                if int(row[6]) != 9999999:
                    if int(row[1]) > 17:
                        if int(row[0]) == 1:
                            incomeDataMale.append(int(row[6]))
                        if int(row[0]) == 2:
                            incomeDataFemale.append(int(row[6]))                        
                        
import matplotlib.pyplot as plt
#https://matplotlib.org/api/_as_gen/matplotlib.pyplot.bar.html
import random
plt.style.use('bmh')
#print(plt.style.available)

maleIncomeSample = random.sample(incomeDataMale, 100)
femaleIncomeSample = random.sample(incomeDataFemale, 100)

alpha = 0.05

maleLower, maleUpper, maleError = getCI(maleIncomeSample, alpha)
femaleLower, femaleUpper, femaleError = getCI(femaleIncomeSample, alpha)
maleIncomeMean = getMean(maleIncomeSample)
femaleIncomeMean = getMean(femaleIncomeSample)

print('The 95% CI for the sample of the income of males is',
      round(maleLower,2), ' to', round(maleUpper,2))
print('The Mean income of males in our sameple is', maleIncomeMean)
print('The 95% CI for the sample of the income of females is',
      round(femaleLower,2), ' to', round(femaleUpper,2))
print('The Mean income of females in our sameple is', femaleIncomeMean)

Labels = ['Male Income', 'Female Income']
means = [maleIncomeMean, femaleIncomeMean]
CIs = [maleError, femaleError]
positions = [0,1]

plt.bar(positions, means, color='grey', yerr=CIs, width=0.5, align = 'center',
        ecolor='black', capsize = 5)

plt.xlabel("Samples")
plt.ylabel("Mean Income ($)")
plt.title("Mean Income Across Different Samples")
plt.xticks(positions, Labels)
plt.show()
















                        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
