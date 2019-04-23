# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 07:37:41 2019

@author: Jacob
"""

import csv

generalPopIncomeData = []
BlackIncomeData = []
with open('usa_00003.csv',newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) > 1:
                if int(row[6]) != 9999999:
                    if int(row[1]) > 17:
                        #if int(row[4]) >= 11:
                        generalPopIncomeData.append(int(row[6]))
                        if int(row[2]) == 2:
                            #if int(row[0])== 2:
                            BlackIncomeData.append(int(row[6]))                    

def getMean(sample):
    sampleSize = len(sample)
    sumTotal = 0
    for row in sample:
        sumTotal = row+sumTotal
    mean = sumTotal/sampleSize
    return mean
    
def getPopSD(sample):
    sampleSize = len(sample)
    sumOfSquares = 0
    mean = getMean(sample)
    for row in sample:
        deviationScore = row - mean
        sumOfSquares = deviationScore**2+sumOfSquares
    variance = sumOfSquares/sampleSize
    popSD = variance**0.5
    return popSD
    
def getSampleSD(sample):
    sampleSize = len(sample)
    sumOfSquares = 0
    mean = getMean(sample)
    for row in sample:
        deviationScore = row - mean
        sumOfSquares = deviationScore**2+sumOfSquares
    variance = sumOfSquares/(sampleSize-1)
    SampleSD = variance**0.5
    return SampleSD    
    


def getPopStandardError(sample):
    sampleSize = len(sample)
    popSD = getPopSD(sample)
    #Standard error of the mean - population
    SEM = popSD/sampleSize**0.5
    return SEM
    
def getSampleStandardError(sample):
    sampleSize = len(sample)
    SampleSD = getSampleSD(sample)
    #Standard error of the mean - sample
    SEM = SampleSD/sampleSize**0.5
    return SEM  
    
#Z = (sampleMean - PopulationMean) / (Standard Error)
def getZScore(sample, population):
    sampleMean = getMean(sample)
    populationMean = getMean(population)
    SEM = getPopStandardError(population)
    Z = (sampleMean-populationMean)/SEM
    return Z

def getProbabilityFromZ(z):
    z = round(float(z),2)
    probability = 0
    if z < -4: 
        return 0.000
    elif z > 4:
        return 1.000
    else:
        with open('z_table.csv', newline='') as zFile:
            zData = csv.reader(zFile)
            for row in zData:
                if z == float(row[0]):
                    probability = float(row[1])
        return probability

def testHypothesis(p,alpha = 0.05, testType='two-tailed'):
    if testType == 'two-tailed':
        if p < (alpha/2) or p > (1-(alpha/2)):
            return True
        else:
            return False
    if testType == 'one-tailed negative':
        if p < alpha:
            return True
        else:
            return False
    if testType == 'one-tailed positive':
        if p > (1-alpha):
            return True
        else:
            return False
    
zScore = getZScore(BlackIncomeData,generalPopIncomeData)  
p = getProbabilityFromZ(zScore)
if testHypothesis(p):
    print('Black income is differnet from the income of the general population'+
          '. We therefore reject the null hypopesis.')
    BlackIncomeMean = getMean(BlackIncomeData)
    generalPopMean =getMean(generalPopIncomeData)
    BlackSampleSize = len(BlackIncomeData)
    genPopSampleSize = len(generalPopIncomeData)
    
    print('Black Income Mean: ',BlackIncomeMean)
    print('Black Income Sample Size: ',BlackSampleSize)
    print('General Population Income Mean: ',generalPopMean)
    print('General Population Income Sample Size: ',genPopSampleSize)
    print('Z Score: ', zScore)
    print('p: ',p)
    
#Hypothesis testing

#There is the null hyposthesis and the alternative hypothesis
#There can three possilbe hyposthese sets
#1 
#Population mean equals the sample mean which supports the null hypothesis
#The population mean does not equal the sample mean which supports the alternative hypothesis
#This is a two tailed test
#2
#The population mean is greater than or equal to the sample mean -supporting the null

    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    