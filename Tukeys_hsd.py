# -*- coding: utf-8 -*-
"""
Created on Wed May  15 14:18:50 2019

@author: Jacob
"""

import math
import scipy.integrate
from decimal import *
import csv
getcontext().prec = 100
import random

def gamma(z):
    def function(t,z):
        e = math.e #2.71828
        return Decimal(t)**(Decimal(z)-Decimal(1))*(Decimal(e)**(Decimal(-t)))
    gam, error = scipy.integrate.quad(function, 0, math.inf,args=(z))
    return gam
    
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
    p, error = scipy.integrate.quad(f_probability_distro_function, 0, f,
                                    args = ((df1,df2)))
    return p
    
def getMean(sample):
    sumTotal = 0
    for row in sample:
        sumTotal+=row
    sampleSize = len(sample)
    mean = sumTotal/sampleSize
    return mean
    
def calculate_f(factor):
    #Using dicts this time - dict = {'key': data, 'nextKey':moreData}
    means = []
    groupSize = len(next(iter(factor.values())))
    for level, values in factor.items():
        mean = getMean(values)
        means.append(mean)
    overAllMean = getMean(means)
    #between groups sum of squares
    betweenGroupSumOfSquares = 0
    for mean in means:
        deviationScore = groupSize*((mean - overAllMean)**2)
        betweenGroupSumOfSquares += deviationScore
    numOfGroups = len(factor)
    #between groups degrees of freedom
    betweenGroupsDF = numOfGroups - 1
    betweenGroupsMeanSquare = betweenGroupSumOfSquares/betweenGroupsDF
    #The within groups part of the f ratio
    withinGroupsSumOfSquares = 0
    for level, values in factor.items():
        for value in values:
            mean = getMean(values)
            deviationScore = value - mean
            withinGroupsSumOfSquares += deviationScore**2
    withinGroupDF = numOfGroups*(groupSize - 1)
    withinGroupMeanSquare = withinGroupsSumOfSquares/withinGroupDF
    F = betweenGroupsMeanSquare/withinGroupMeanSquare
    return F
    
def oneWayANOVA(factor, alpha):
    significant  = False 
    F = calculate_f(factor)
    dfBetween = len(factor)-1
    dfWithin = len(factor)*(len(next(iter(factor.values())))-1)
    #Shortcut to deal with computers not liking really big numbers
    dfWithinUsed = dfWithin
    if dfWithinUsed >=300:
        print('Warning: dfWithin set to 300 to prevent math overflow error')
        dfWithinUsed = 300
    p = getPFromF(F, dfBetween, dfWithinUsed)
    if p > (1-alpha):
        significant  = True
    return round(p,7), round(F, 4), significant, dfBetween, dfWithin
    
#Standard normal distro pdf and cdf
def snd_pdf(x):
    return (1/((2*math.pi)**0.5))*(math.e**(-0.5*(x**2)))
    
def snd_cdf(x):
    return (1+math.erf(x/2**0.5))/2
    
#Studentized range distribution cdf
def srd_cdf_poly_two(q, df, numGroups):
    def f(x, q, df, numGroups):
        func1 = (x**(df-1))*math.e**(-(df*x**2)/2)
        def subPolyTwo(u,x,q,numGroups):
            subPoly = snd_pdf(u)*(snd_cdf(u) - snd_cdf(u-q*x))**(numGroups-1)
            return subPoly
        func2,error = scipy.integrate.quad(subPolyTwo, -math.inf, math.inf,
                                           args=(x,q,numGroups))
        func = func1*func2
        return func
    polyTwo,error = scipy.integrate.quad(f, 0, math.inf, args=(q,df,numGroups))
    return polyTwo

def srd_cdf(q, numGroups, df):
    if df > 115: df = 116
    polyOne = (numGroups*df**(df/2))/(math.gamma(df/2)*2**(df/2-1))
    polyTwo = srd_cdf_poly_two(q,df,numGroups)
    p = polyOne*polyTwo
    return p

def calculate_qs(factor):
    #q is the positive difference between two means within a collection of means
    #divided by the standard error of the means
    numGroups = len(factor)
    groupSize = len(next(iter(factor.values())))
    means = {} #dict NOT list
    for level, values in factor.items():
        mean = getMean(values)
        means[level] = mean # key: data
    withinGroupsSumOfSquares = 0
    for level, values in factor.items():
        for value in values:
            mean = getMean(values)
            deviationScore = value - mean
            withinGroupsSumOfSquares += deviationScore**2
    withinGroupsDF = numGroups*(groupSize-1)
    #wGMS = within groups mean square
    wGMS = withinGroupsSumOfSquares/withinGroupsDF
    #Need to assume groups are the same size
    #If this is not the case, use Tukey-Kramer method
    denom = (wGMS/groupSize)**0.5
    qs = {}
    for mean, value in means.items():
        for other, otherValues in means.items():
            if value != otherValues: # not looking at the same mean twice
                q = round(abs(value - otherValues)/denom,4)
                if q not in qs.values():
                    key = mean+' by '+other
                    qs[key]=round(q,4)
    return qs
    
def tukeys_hsd(factor, alpha):
    Qs = calculate_qs(factor)
    groupSize = len(next(iter(factor.values())))
    numGroups = len(factor)
    df = numGroups*(groupSize-1)
    if df > 349: df = 349
    significantQs = {}
    for key, value in Qs.items():
        p = srd_cdf(value, numGroups, df)
        if p >= 1-alpha:
            significantQs[key] = [round(1-p,4), value]
    return significantQs
    
#First example using dictionaries!

fullRaceFactor = {
                  'white':[],
                  'black':[],
                  'americian_indian':[],
                  'chinese':[],
                  'japanese':[],
                  'other_asian':[],
                  'other_race':[],
                  'two_races':[],
                  'three_races':[]
                  }    
    
with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT': #filter out header
            if int(row[6]) != 9999999: # Filter out N/A
                if int(row[6]) > 1: #Only looking at people who earned money in 2017
                    if int(row[1]) > 17: #Looking at adults only
                        if int(row[2]) == 1: #filtering each race
                            fullRaceFactor['white'].append(int(row[6]))
                        elif int(row[2]) == 2:
                            fullRaceFactor['black'].append(int(row[6]))
                        elif int(row[2]) == 3:
                            fullRaceFactor['americian_indian'].append(int(row[6]))    
                        elif int(row[2]) == 4:
                            fullRaceFactor['chinese'].append(int(row[6]))    
                        elif int(row[2]) == 5:
                            fullRaceFactor['japanese'].append(int(row[6]))    
                        elif int(row[2]) == 6:
                            fullRaceFactor['other_asian'].append(int(row[6]))    
                        elif int(row[2]) == 7:
                            fullRaceFactor['other_race'].append(int(row[6]))    
                        elif int(row[2]) == 8:
                            fullRaceFactor['two_races'].append(int(row[6]))    
                        elif int(row[2]) == 9:
                            fullRaceFactor['three_races'].append(int(row[6]))      
                            
sampleSize = 100
sampleRaceFactor = {
'whiteSample':random.sample(fullRaceFactor['white'],sampleSize),
'blackSample':random.sample(fullRaceFactor['black'], sampleSize),
'americian_indianSample':random.sample(fullRaceFactor['americian_indian'], sampleSize),
'chineseSample':random.sample(fullRaceFactor['chinese'], sampleSize),
'japaneseSample':random.sample(fullRaceFactor['japanese'], sampleSize),
'other_asianSample':random.sample(fullRaceFactor['other_asian'], sampleSize),
'other_raceSample':random.sample(fullRaceFactor['other_race'], sampleSize),
'two_racesSample':random.sample(fullRaceFactor['two_races'], sampleSize),
'three_racesSample':random.sample(fullRaceFactor['three_races'], sampleSize)
}

alpha = 0.05

p, F, significance, dfBetween, dfWithin = oneWayANOVA(sampleRaceFactor, alpha)

if significance:
    #Same as last video
    print('There were statistically significant differences between group means',
          ' as determined by a one-way ANOVA F(',dfBetween,',',dfWithin,') =',F,
          ', p =',round(1-p,7))
    #Now with significant results, we use Tukey's HSD
    print("Tukey's HSD results: \n")
    sigEffects = tukeys_hsd(sampleRaceFactor, alpha)
    for key, value in sigEffects.items():
        print(key, 'was significant with q =', value[1],'and p =',value[0])
        
if not significance:
    #Same as last week
    print('There were no statistically significant differences between group means',
          ' as determined by a one-way ANOVA F(',dfBetween,',',dfWithin,') =',F,
          ', p =',round(1-p,7))
    #Post hoc test is not needed in this situation    
    
    
    
    
    
    
    
    
    
    
    
    
    
    













    




























                            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    