# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:43:08 2019

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
        sumOfSquares+=deviationScore**2
    variance = sumOfSquares/(sampleSize-1)
    return variance
    
def getSampleSD(sample):
    sampleSize = len(sample)
    mean = getMean(sample)
    sumOfSquares = 0
    for row in sample:
        deviationScore = row - mean
        sumOfSquares+=deviationScore**2
    variance = sumOfSquares/(sampleSize-1)
    sd = variance**0.5
    return sd 
    
def getSampleStandardError(sample):
    sampleSD = getSampleSD(sample)
    sampleSize = len(sample)
    SEM = sampleSD/sampleSize**0.5
    return SEM
    
def getPooledSD(sample1, sample2):
    variance1 = getSampleVariance(sample1)
    variance2 = getSampleVariance(sample2)
    sampleSize1 = len(sample1)
    sampleSize2 = len(sample2)
    if sampleSize1 == sampleSize2:
        pooledVariance = (variance1 + variance2)/2
        pooledSD = pooledVariance**0.5
    else:
        numerator = (sampleSize1 - 1)*variance1 + (sampleSize2 - 1)*variance2
        denominator = sampleSize1 + sampleSize2 - 2 #df for this test
        pooledSD= (numerator/denominator)**0.5
    return pooledSD
    
def twoIndependentSamplesTScore(sample1, sample2):
    mean1 =getMean(sample1)
    mean2 = getMean(sample2)
    sampleSize1 = len(sample1)
    sampleSize2 = len(sample2)
    pooledSD = getPooledSD(sample1, sample2)
    if sampleSize1 == sampleSize2:
        pooledSE = pooledSD*((2/sampleSize1)**0.5)
        t = (mean1 - mean2)/pooledSE
    else:
        print('Warning: Unequal Sample Sizes')
        pooledSE = pooledSD*(((1/sampleSize1)+(1/sampleSize2))**0.5)
        t = (mean1-mean2)/pooledSE
    return t
    
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
    elif testType == 'one-tailed positive':
        with open('t_table.csv',newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0]) == df:
                    if float(row[2]) >= float(alpha):
                        criticalT = float(row[1])
                        break     
    return criticalT
    
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
    
def twoIndependentSamplesTTest(sample1, sample2, alpha, testType = 'two-tailed'):
    sampleSize1 = len(sample1)
    sampleSize2 = len(sample2)
    df = sampleSize1 + sampleSize2 - 2
    critT = getCriticalT(alpha, df, testType)
    t = twoIndependentSamplesTScore(sample1, sample2)    
    p = getPFromT(t,df)
    
    significant = False
    if testType == 'two-tailed':
        if t < -critT or t > critT:
            significant = True
    elif testType == 'one-tailed positive':
        if t > critT:
            significant = True
    elif testType == 'one-tailed negative':
        if t < -critT:
            significant = True
    return significant, t, critT, p
    
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
    
#For the example today:

japaneseMaleIncomeData = []
japaneseFemaleIncomeData = []

with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT': #Filter out the header
            if int(row[6]) > 1: #Looking only at people who made money in 2017
                if int(row[6]) != 9999999: #filter out N/A replies
                    if int(row[1]) > 17: #looking at 18+ y/o
                        if int(row[2]) ==5: #if they are japanese
                            if int(row[0]) == 1: #if they are male
                                japaneseMaleIncomeData.append(int(row[6]))
                            if int(row[0]) == 2: #if they are female
                                japaneseFemaleIncomeData.append(int(row[6]))
                                
import random
japaneseMaleIncomeSample = random.sample(japaneseMaleIncomeData,100)
japaneseFemaleIncomeSample = random.sample(japaneseFemaleIncomeData, 100)

japanMaleMean = getMean(japaneseMaleIncomeSample)                         
japanFealeMean = getMean(japaneseFemaleIncomeSample)                               

alpha = 0.05
testType = 'two-tailed'

sigBool, t, criticalT, p = twoIndependentSamplesTTest(japaneseMaleIncomeSample,
                                                      japaneseFemaleIncomeSample,
                                                      alpha, testType)

if sigBool:
    print('The two sample independent means T test was significiant at alpha=',
          alpha, ' where p=', round((1-p),5),' and t=', round(t,2),'.\nCritical T:',
          criticalT,'\nMean Income For Japanese Males:', round(japanMaleMean,2),
          '\nMean Income For Japanese Females:', round(japanFealeMean,2))

if not sigBool:
    print('The two sample independent means T test was NOT significiant at alpha=',
          alpha, ' where p=', round(p,5),' and t=', round(t,2),'.\nCritical T:',
          criticalT,'\nMean Income For Japanese Males:', round(japanMaleMean,2),
          '\nMean Income For Japanese Females:', round(japanFealeMean,2))

#CIs
japanMaleLower, japanMaleUpper, japanMaleError = getCI(japaneseMaleIncomeSample, alpha)
japanFemaleLower, japanFemaleUpper, japanFemaleError = getCI(japaneseFemaleIncomeSample, alpha)

import matplotlib.pyplot as plt
plt.style.use('bmh')

Labels = ['Japanese Male Income', 'Japanese Female Income']
means = [japanMaleMean, japanFealeMean]
CIs = [japanMaleError, japanFemaleError]
positions = [0,1]

plt.bar(positions, means, color = 'grey', yerr=CIs, width=0.5, align='center',
        ecolor='black', capsize=5)

plt.xlabel('Male and Female Japanese American Income')
plt.ylabel('Mean Income ($)')
plt.title('Mean Income Across Male and Female Japanese Americans')
plt.xticks(positions, Labels)
plt.show()









