# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:59:33 2019

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
    sampleSD = variance**0.5
    return sampleSD
    
def getSampleStandardError(sample):
    sampleSD = getSampleSD(sample)
    sampleSize = len(sample)
    SEM = sampleSD/sampleSize**0.5
    return SEM
    
#New
def getDeltaSD(sample1, sample2):
    sampleSize1 = len(sample1)
    sampleSize2 = len(sample2)
    variance1 = getSampleVariance(sample1)
    variance2 = getSampleVariance(sample2)
    
    deltaSD = (variance1/sampleSize1 + variance2/sampleSize2)**0.5
    return deltaSD
    
#pooled degrees of freedom. Also called the Welch-Satterthwaite equation
def getPooledDF(sample1, sample2):
    sampleSize1 = len(sample1)
    sampleSize2 = len(sample2)
    variance1 = getSampleVariance(sample1)
    variance2 = getSampleVariance(sample2)
    
    numerator = (variance1/sampleSize1 + variance2/sampleSize2)**2
    d1 = ((variance1/sampleSize1)**2)/(sampleSize1 - 1)
    d2 = ((variance2/sampleSize2)**2)/(sampleSize2 - 1)
    denominator = d1 + d2
    df = numerator/denominator
    return df
    
#welch's t-test for when two population variances are not assumed to be equal
def unequalVarianceTScore(sample1, sample2):
    mean1 = getMean(sample1)
    mean2 = getMean(sample2)
    deltaSD = getDeltaSD(sample1, sample2)
    t = (mean1 - mean2)/deltaSD
    return t

#Getting the critical t is the same as in previous videos
def getCriticalT(alpha, df, testType = 'two-tailed'):
    df = round(df)
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
        print('true')
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

#Figuring out our p score is also the same as in previous videos
def getPFromT(t, df):
    df = round(df)
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

#Rather than something like "t test" we are just calling this significance test
def significanceTest(sample1, sample2, alpha, testType='two-tailed'):
    #differnt from previous videos
    df = getPooledDF(sample1, sample2)
    critT = getCriticalT(alpha, df, testType)
    t = unequalVarianceTScore(sample1, sample2)
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
    
#same as in our earlier videos
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

#example for today: male vs female income for whites
whiteMaleIncome = []
whiteFemaleIncome = []
with open('usa_00003.csv',newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':#filter header
            if int(row[6]) > 1:#filter incomes less than 1
                if int(row[6]) != 9999999:#filter N/A
                    if int(row[1]) > 17:#filter minors
                        if int(row[2]) == 1:#if they are white
                            if int(row[0]) == 1:#if they are male
                                whiteMaleIncome.append(int(row[6]))
                            if int(row[0]) == 2:#if they are female
                                whiteFemaleIncome.append(int(row[6]))
                                
import random 
#because this dataset is massive, we are taking a smaller sample from it
#for the purpose of this tutorial
whiteMaleIncomeSample = random.sample(whiteMaleIncome,50)
whiteFemaleIncomeSample = random.sample(whiteFemaleIncome,50)

whiteMaleMean = getMean(whiteMaleIncomeSample)
whiteFemaleMean = getMean(whiteFemaleIncomeSample)

alpha = 0.05
testType = 'one-tailed positive'

sigBool, t, criticalT, p = significanceTest(whiteFemaleIncomeSample,
                                            whiteMaleIncomeSample,
                                            alpha, testType)
#Very similar to previous videos
if sigBool:
    print('The two sample independent means, unequal variances, t test '+
          'was significant at alpha =', alpha, ', where p =', round(1-p,5),
          'and t = ', round(t,2),'.\nCritical T:', criticalT,
          '\nMean Income for White Males:',round(whiteMaleMean,2),
          '\nMean Income for White Females:',round(whiteFemaleMean,2))

if not sigBool:
    print('The two sample independent means, unequal variances, t test '+
          'was NOT significant at alpha =', alpha, ', where p =', round(p,5),
          'and t = ', round(t,2),'.\nCritical T:', criticalT,
          '\nMean Income for White Males:',round(whiteMaleMean,2),
          '\nMean Income for White Females:',round(whiteFemaleMean,2))

#Graph with CIs
whiteMaleLower, whiteMaleUpper, whiteMaleError = getCI(whiteMaleIncomeSample, alpha)
whiteFemaleLower, whiteFemaleUpper, whiteFemaleError = getCI(whiteFemaleIncomeSample, alpha)

import matplotlib.pyplot as plt
plt.style.use('bmh')

labels = ['White Male Income', 'White Female Income']
means = [whiteMaleMean, whiteFemaleMean]
CIs = [whiteMaleError, whiteFemaleError]
positions = [0,1]

plt.bar(positions, means, color='grey', yerr=CIs, width=0.5, align='center',
        ecolor='black', capsize=5)

plt.xlabel('Male and Female White American Income')
plt.ylabel('Mean Income ($)')
plt.title('Mean Income Across Male and Female White Americans')
plt.xticks(positions, labels)
plt.show()


















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    