# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:20:03 2019

@author: Jacob
"""

import csv

def getMean(sample):
    sampleSize = len(sample)
    sumTotal = 0
    for row in sample:
        sumTotal+=row
    mean = sumTotal/sampleSize
    return mean
    
def getSampleSD(sample):
    sampleSize = len(sample)
    mean = getMean(sample)
    sumOfSquares = 0
    for row in sample:
        deviationScore = row - mean
        sumOfSquares+=deviationScore**2
    variance = sumOfSquares/(sampleSize-1)
    sampleSD=variance**0.5
    return sampleSD
    
def getSampleStandardError(sample):
    sampleSD = getSampleSD(sample)
    sampleSize = len(sample)
    SEM = sampleSD/sampleSize**0.5
    return SEM
    
def getCriticalT(alpha, sample, testType = 'two-tailed'):
    sampleSize = len(sample)
    df = sampleSize - 1
    if df > 120:
        df = 120
    criticalT = 0
    if testType == 'two-tailed':
        with open('t_table.csv', newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0])==df:
                    if float(row[2])>=float(1-(alpha/2)):
                        criticalT=float(row[1])
                        break           
    elif testType == 'one-tailed positive':
        with open('t_table.csv', newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0])==df:
                    if float(row[2])>=float(1-(alpha)):
                        criticalT=float(row[1])
                        break                    
    elif testType == 'one-tailed negative':
        with open('t_table.csv', newline='') as tFile:
            tData = csv.reader(tFile)
            for row in tData:
                if int(row[0])==df:
                    if float(row[2])>=float(alpha):
                        criticalT=float(row[1])
                        break 
    return criticalT

def getPFromT(t,df):
    p = None
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
                    if float(row[1])== round(float(t),2):
                        p = float(row[2])
                        break
    return p
    
def oneSampleTTest(sample, popMean, alpha, testType = 'two-tailed'):
    sampleMean= getMean(sample)
    sampleSize = len(sample)
    SEM = getSampleStandardError(sample)
    df = sampleSize-1
    significant = False
    t=(sampleMean-popMean)/SEM
    p = getPFromT(t,df)
    critT = getCriticalT(alpha, sample, testType)
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
    

generalPopIncomeData = []
blackFemaleIncomeData = []

with open('usa_00003.csv',newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) > 1:
                if int(row[6]) != 9999999:
                    if int(row[1]) > 17:
                        generalPopIncomeData.append(int(row[6]))
                        if int(row[2]) == 2: #If they are black
                            if int(row[0]) == 2: #if they are female
                                blackFemaleIncomeData.append(int(row[6]))

import random

blackFemaleIncomeSample = random.sample(blackFemaleIncomeData, 30)
popMean = getMean(generalPopIncomeData)
sampleMean = getMean(blackFemaleIncomeSample)
alpha = 0.05
testType = 'two-tailed'

sigBool, sampleT, criticalT, p = oneSampleTTest(blackFemaleIncomeSample,
                                                popMean, alpha, testType)

if sigBool:
    print('The one sample T test is significant at alpha =', alpha,
          ' where p=',p,' and t=', round(sampleT,2),'.\nCritical T:',criticalT,
          '\nSample Mean:',sampleMean,'\nPopulation Mean:',round(popMean,2))
if not sigBool:
    print('The one sample T test is NOT significant at alpha =', alpha,
          ' where p=',p,' and t=', round(sampleT,2),'.\nCritical T:',criticalT,
          '\nSample Mean:',sampleMean,'\nPopulation Mean:',round(popMean,2))



















                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
















                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    