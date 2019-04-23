# -*- coding: utf-8 -*-
"""
Created on Fri Apr  10 22:32:11 2019

@author: Jacob
"""

from math import gamma
from decimal import *
import csv
import scipy.integrate

getcontext().prec = 100

def f_probability_distro_function(f, df1, df2):
    top = ((Decimal(df1)*Decimal(f))**Decimal(df1))*(Decimal(df2)**Decimal(df2))
    bottom = (Decimal(df1)*Decimal(f)+Decimal(df2))**(Decimal(df1)+Decimal(df2))
    num = (Decimal(top)/Decimal(bottom))**Decimal(0.5)
    a = df1/2
    b = df2/2
    beta = (gamma(a)*gamma(b))/gamma(a+b)
    denom = f*beta
    pdf = float(num)/float(denom)
    return pdf
    
def getPFromF(f,df1,df2):
    probability, error = scipy.integrate.quad(f_probability_distro_function, 0, f,
                                              args=((df1,df2)))
    return probability
    
def getMean(sample):
    sumTotal = 0
    for row in sample:
        sumTotal+=row
    sampleSize = len(sample)
    mean = sumTotal/sampleSize
    return mean
    
def calculate_f(factor):
    #calculate mean for each level of the factor
    means = []
    groupSize = len(factor[0])
    for level in factor:
        mean = getMean(level)
        means.append(mean)
    overAllMean = getMean(means)
    #Between group sum of squares
    betweenGroupSumOfSquares = 0
    for mean in means:
        deviationScore = groupSize*((mean - overAllMean)**2)
        betweenGroupSumOfSquares += deviationScore
    numOfGroups = len(factor)
    #between groups degrees of freedom
    betweenGroupsDF = numOfGroups - 1
    betweenGroupsMeanSquare = betweenGroupSumOfSquares/betweenGroupsDF
    withinGroupsSumOfSquares = 0
    for mean,level in zip(means, factor):
        for value in level:
            deviationScore = value - mean
            withinGroupsSumOfSquares += deviationScore**2
    withinGroupsDF = numOfGroups*(groupSize - 1)
    withinGroupMeanSquare = withinGroupsSumOfSquares/withinGroupsDF
    #And finally the f ratio!
    F = betweenGroupsMeanSquare/withinGroupMeanSquare
    return F, betweenGroupsMeanSquare, withinGroupMeanSquare
    
def oneWayANOVA(factor, alpha):
    significant = False
    F, betweenGroupsMeanSquare, withinGroupMeanSquare = calculate_f(factor)
    dfBetween = len(factor) - 1
    dfWithin = len(factor)*(len(factor[0])-1)
    dfWithinUsed = dfWithin
    if dfWithinUsed >= 300:
        print('Warning: dfWithin set to 300 to prevent a math overflow error.\n')
        dfWithinUsed = 300
    p = getPFromF(F, dfBetween, dfWithinUsed)
    if p > (1-alpha):
        significant = True
    return round(p,7), round(F, 4), significant, dfBetween, dfWithin
    
#Example for today
white = []#1
black = []#2
americian_indian = []#3
chinese = [] #4
japanese = [] #5
other_asian = [] #6
other_race = [] #7
two_races = [] #8
three_races = [] #9

with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT': #Filter out the header
            if int(row[6]) != 9999999: #Filter out N/A replies
                if int(row[6]) > 1: #Looking only at people who earned income in 2017
                    if int(row[1]) > 17: #looking at 18 y/o only
                        if int(row[2]) == 1: #filtering each race
                            white.append(int(row[6]))
                        elif int(row[2]) == 2:
                            black.append(int(row[6]))
                        elif int(row[2]) == 3:
                            americian_indian.append(int(row[6]))                            
                        elif int(row[2]) == 4:
                            chinese.append(int(row[6]))        
                        elif int(row[2]) == 5:
                            japanese.append(int(row[6]))        
                        elif int(row[2]) == 6:
                            other_asian.append(int(row[6]))        
                        elif int(row[2]) == 7:
                            other_race.append(int(row[6]))        
                        elif int(row[2]) == 8:
                            two_races.append(int(row[6]))        
                        elif int(row[2]) == 9:
                            three_races.append(int(row[6]))      
                            
import random 
sampleSize = 100

whiteSample = random.sample(white, sampleSize)
blackSample = random.sample(black, sampleSize)
americian_indianSample = random.sample(americian_indian, sampleSize)
chineseSample = random.sample(chinese, sampleSize)
japaneseSample = random.sample(japanese, sampleSize)
other_asianSample = random.sample(other_asian, sampleSize)
other_raceSample = random.sample(other_race, sampleSize)
two_racesSample = random.sample(two_races, sampleSize)
three_racesSample = random.sample(three_races, sampleSize)

raceFactor = []

raceFactor.append(whiteSample)
raceFactor.append(blackSample)
raceFactor.append(americian_indianSample)
raceFactor.append(chineseSample)
raceFactor.append(japaneseSample)
raceFactor.append(other_asianSample)
raceFactor.append(other_raceSample)
raceFactor.append(two_racesSample)
raceFactor.append(three_racesSample)

alpha = 0.05

p, F, significance, dfBetween, dfWithin = oneWayANOVA(raceFactor, alpha)

if significance:
    #We will start on ad hoc tests next video
    print('There were statistically significant differences between group means',
          ' as determined by a one-way ANOVA F(',dfBetween,',',dfWithin,') =',F,
          ', p =',round(1-p,7))

if not significance:
    print('There were no statistically significant differences between group means',
          ' as determined by a one-way ANOVA F(',dfBetween,',',dfWithin,') =',F,
          ', p =',round(1-p,7))











                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
