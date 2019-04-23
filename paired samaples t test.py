# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:52:25 2019

@author: Jacob
"""

import csv

def getMean(sample):
    sumTotal = 0
    sampleSize = len(sample)
    for row in sample:
        sumTotal+=row
    mean = sumTotal/sampleSize
    return mean
    
def getSampleVariance(sample):
    sampleSize = len(sample)
    mean = getMean(sample)
    sumOfSquares = 0
    for row in sample:
        deviationScore = row - mean
        sumOfSquares += deviationScore**2
    variance = sumOfSquares/(sampleSize - 1)
    return variance
    
def getSampleSD(sample):
    variance = getSampleVariance(sample)
    SD = variance**0.5
    return SD
    
def getSampleStandardError(sample):
    sampleSD = getSampleSD(sample)
    sampleSize = len(sample)
    SEM = sampleSD/sampleSize**0.5
    return SEM
    
def getDifferenceScores(sample):
    differenceScores = []
    for row in sample:
        before = row[0]
        after = row[1]
        differenceScore = after - before
        differenceScores.append(differenceScore)
    return differenceScores
    
def pairedSamplesTScore(sample):
    sampleSize = len(sample)
    differenceScores = getDifferenceScores(sample)
    meanDifference = getMean(differenceScores)
    SDDifference = getSampleSD(differenceScores)
    mu = 0
    t = (meanDifference - mu)/(SDDifference/(sampleSize**0.5))
    return t
    
#Getting the critical t is the same as before
def getCriticalT(alpha, df, testType = 'two-tailed'):
    if df > 120:
        df = 120
    criticalT = 0
    if testType == 'two-tailed':
        with open('t_table.csv',newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0]) == df:
                    if float(row[2]) >= float(1-(alpha/2)):
                        criticalT = float(row[1])
                        break
    elif testType == 'one-tailed positive':
        with open('t_table.csv',newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0]) == df:
                    if float(row[2]) >= float(1-(alpha)):
                        criticalT = float(row[1])
                        break    
    elif testType == 'one-tailed negative':
        with open('t_table.csv',newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0]) == df:
                    if float(row[2]) >= float(alpha):
                        criticalT = float(row[1])
                        break     
    return criticalT    

#Finding our p value is also the same as before
def getPFromT(t, df):
    if df > 120:
        df = 120
    if t > 6:
        p = 1.0
        
    elif t < -6:
        p = 0.0
        
    elif t > -6 and t < 6:
        with open('t_table.csv', newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0]) == df:
                    if float(row[1]) == round(float(t),2):
                        p = float(row[2])
                        
                        break
    return p  

#Our significance test is the same as before
def significanceTest(sample, alpha, testType='two-tailed'):
    sampleSize = len(sample)

    df = sampleSize - 1
    critT = getCriticalT(alpha, df, testType)
    t = pairedSamplesTScore(sample)
    p = getPFromT(t, df)
    significant = False 
    
    if testType == 'two-tailed':
        if t < -critT or t > critT:
            significant = True
    elif testType == 'one-tailed positive':
        if t > critT:
            significant = True
    elif testType == 'one-tailed negative':
        if t < critT:
            significant = True
    return significant, t, critT, p

#The function for our CIs is still the same
def getCI(sample, alpha):
    mean = getMean(sample)
    SEM = getSampleStandardError(sample)
    df = len(sample)-1
    testType = 'two-tailed'
    critT = getCriticalT(alpha, df, testType)
    lowerCI = mean - critT*SEM
    upperCI = mean + critT*SEM
    error = critT*SEM
    return lowerCI, upperCI, error

#Example for today: Super amazing financial advice

incomeData = []
with open('usa_00003.csv',newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) > 1:
                if int(row[6]) != 9999999:
                    if int(row[1]) > 17:
                        incomeData.append(int(row[6]))
                        
import random

incomeDataSample = random.sample(incomeData, 24)

incomeAfterTreatment = []
for row in incomeDataSample:
    treatmentImpact = random.randint(-200,500)
    afterAdviceIncome = row + treatmentImpact
    incomeAfterTreatment.append(afterAdviceIncome)
    
aggregatedIncomeData = []
i = 0
for row in incomeDataSample:
    new_row = [row, incomeAfterTreatment[i]]
    i+=1
    aggregatedIncomeData.append(new_row)
    
incomeSampleMean = getMean(incomeDataSample)
incomeAfterTreatmentMean = getMean(incomeAfterTreatment)

alpha = 0.05
testType = 'one-tailed positive'

sigBool, t, criticalT, p = significanceTest(aggregatedIncomeData, alpha, 
                                            testType)

#Very similar to previous videos

if sigBool:
    print('The Dependent T-Test for paired samples was significant at'+
          ' alpha =', alpha, 'where p =', round(p,5), 'and t =', round(t,2),
          '\nCritical T =', criticalT,
          '\nMean income before Awesome Advice:', round(incomeSampleMean, 2),
          '\nMean income after Awesome Advice:', round(incomeAfterTreatmentMean,2))

if not sigBool:
    print('The Dependent T-Test for paired samples was NOT significant at'+
          ' alpha =', alpha, 'where p =', round(p,5), 'and t =', round(t,2),
          '\nCritical T =', criticalT,
          '\nMean income before Awesome Advice:', round(incomeSampleMean, 2),
          '\nMean income after Awesome Advice:', round(incomeAfterTreatmentMean,2))

#Other than the names and labels, this is exactly the same as before
beforeLower, beforeUpper, beforeError = getCI(incomeDataSample, alpha)
afterLower, afterUpper, afterError = getCI(incomeAfterTreatment, alpha)

import matplotlib.pyplot as plt
plt.style.use('bmh')

labels = ['Before Advice Income', 'After Advice Income']
means = [incomeSampleMean, incomeAfterTreatmentMean]
CIs = [beforeError, afterError]
positions = [0,1]

plt.bar(positions, means, color='grey', yerr=CIs, width=0.5, align='center',
        ecolor='black', capsize=5)

plt.xlabel('Average Income Before and After Advice')
plt.ylabel('Mean Income ($)')
plt.title('Mean Income Before and After Advice')
plt.xticks(positions, labels)
plt.show()




















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    