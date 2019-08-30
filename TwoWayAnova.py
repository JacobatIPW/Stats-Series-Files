# -*- coding: utf-8 -*-
"""
Created on Mon Aug  20 13:25:17 2019

@author: Jacob
"""

import math
import scipy.integrate
from decimal import *
import csv
import random
from collections import OrderedDict

getcontext().prec = 100

def gamma(z):
    def function(t,z):
        e = math.e #2.71828
        return Decimal(t)**(Decimal(z)-Decimal(1))*(Decimal(e)**(Decimal(-t)))
    gam, error = scipy.integrate.quad(function,0,math.inf, args=(z))
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
    
def getPFromF(f, df1, df2):
    p, error = scipy.integrate.quad(f_probability_distro_function, 0, f, 
                                    args=((df1,df2)))
    return p
    
def getMean(sample):
    total = 0
    for row in sample:
        total+= row
    mean = total/len(sample)
    return mean
    
def TwoWayANOVA(data, alpha, getP):
    model = OrderedDict()
    grandMean = 0
    i = 0 # i=0 all data, i=1 factors, i=2 cells
    #If you were watching below, in builing the sample, we reversed the order
    #so we are reversing it again to fix this, it is not needed normalally
    for key, datum in reversed(data.items()):
        if i == 0: #Getting the grand mean and SS total
            grandMean = getMean(datum)
            sumOfSquaresTotal = 0
            for row in datum:
                sumOfSquaresTotal += (row - grandMean)**2
            model['total'] = [sumOfSquaresTotal]
            
        if i == 1:#Looking at the factors
            model['factors'] = OrderedDict()
            for factor, factorLevels in datum.items():
                model['factors'][factor] = []
                ssFactor = 0
                for level, levelData in factorLevels.items():
                    factorMean = getMean(levelData)
                    sumOfSquares = len(levelData)*(factorMean-grandMean)**2
                    ssFactor += sumOfSquares
                factorDF = len(factorLevels) - 1
                meanSquare = ssFactor/factorDF
                model['factors'][factor].append(ssFactor)
                model['factors'][factor].append(factorDF)
                model['factors'][factor].append(meanSquare)
                
        if i == 2: #Each Cell
            sumOfSquaresWithin = 0
            dfWithin = 0
            model['cells'] = OrderedDict()
            for cell, cellData in datum.items():
                cellMean = getMean(cellData)
                cellSumOfSquares = 0
                dfWithin += len(cellData) - 1
                for row in cellData:
                    cellSumOfSquares += (row - cellMean)**2
                model['cells'][cell] = [cellMean]
                sumOfSquaresWithin += cellSumOfSquares
            msWithin = sumOfSquaresWithin/dfWithin
        i +=1
    
    significance = False
    for key, row in model['factors'].items():
        F = row[2]/msWithin
        if getP:
            print('calculating p')
            p = 1 - getPFromF(F, row[1], dfWithin)
            if p < alpha: significance = True
            print('p for ', key, 'is ', p)
            p = round(p,4)
        else:
            p = 'NaN'
        model['factors'][key].append(round(F,4))
        model['factors'][key].append(p)
        model['factors'][key].append(significance)
        significance = False
        
    ssAllFactors = 0
    for key, row in model['factors'].items(): ssAllFactors - row[0]
    ssAllFactors = ssAllFactors - sumOfSquaresWithin
    ssAllFactors = ssAllFactors + sumOfSquaresTotal
    
    dfAllFactors = 1
    for key, row in model['factors'].items(): dfAllFactors *= row[1]
    msAllFactors = ssAllFactors/dfAllFactors
    FAllFactors = ssAllFactors/msWithin
    
    if getP:
        print('calculating interaction p')
        pAllFactors = 1 - getPFromF(F, dfAllFactors, dfWithin)
        if pAllFactors < alpha: significance = True
        print('p interaction:', pAllFactors)
        pAllFactors = round(pAllFactors,4)
    else:
        pAllFactors = 'NaN'
        
    dfTotal = 0
    for key, row in model['factors'].items(): dfTotal += row[1]
    dfTotal += dfWithin
    dfTotal += dfAllFactors
    model['total'].append(dfTotal)
    
    model['interaction'] = [ssAllFactors, dfAllFactors, msAllFactors,
                            round(FAllFactors,4), pAllFactors,
                            significance]
                            
    model['within(error)'] = [sumOfSquaresWithin, dfWithin, msWithin]
    
    return model, dfWithin
    
genderByRace = OrderedDict()
genderByRace['gender_by_race'] = []
genderByRace['factors'] = OrderedDict()
genderByRace['factors']['gender'] = OrderedDict()
genderByRace['factors']['gender']['male'] = []
genderByRace['factors']['gender']['female'] = []
genderByRace['factors']['race'] = OrderedDict()
genderByRace['factors']['race']['white'] = []
genderByRace['factors']['race']['black'] = []
genderByRace['cells'] = OrderedDict()
genderByRace['cells']['white_male'] = []
genderByRace['cells']['white_female'] = []
genderByRace['cells']['black_male'] = []
genderByRace['cells']['black_female'] = []

with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT': #filter out header
            if int(row[6]) != 9999999: #Filter out N/A
                if int(row[6]) > 1: #Only people who earned money in 2017
                    if int(row[1]) > 17: #Looking at 18+ years old
                        if int(row[4]) == 11: #To narrow down more we are only
                        #looking at people with 5+ years of education
                            genderByRace['gender_by_race'].append(int(row[6]))
                            
                            if int(row[0])==1:
                                genderByRace['factors']['gender']['male'].append(int(row[6]))
                            if int(row[0])==2:
                                genderByRace['factors']['gender']['female'].append(int(row[6]))

                            if int(row[2])==1:
                                genderByRace['factors']['race']['white'].append(int(row[6]))
                            if int(row[2])==2:
                                genderByRace['factors']['race']['black'].append(int(row[6]))

                            if int(row[2])==1 and int(row[0]) == 1:
                                genderByRace['cells']['white_male'].append(int(row[6]))
                            if int(row[2])==1 and int(row[0]) == 2:
                                genderByRace['cells']['white_female'].append(int(row[6]))
                            if int(row[2])==2 and int(row[0]) == 1:
                                genderByRace['cells']['black_male'].append(int(row[6]))
                            if int(row[2])==2 and int(row[0]) == 2:
                                genderByRace['cells']['black_female'].append(int(row[6]))

#If your sample was collected with a two way ANOVA in mind, then you you can more
#more or less skip the following.
#However, we need to have each cell be the same size and we are going to resample
#from our 3 million dataset

cellSampleSize = 200

balancedSample = OrderedDict()

balancedSample['cells'] = OrderedDict()
balancedSample['cells']['white_male'] = random.sample(genderByRace['cells']['white_male'],cellSampleSize)
balancedSample['cells']['white_female'] = random.sample(genderByRace['cells']['white_female'],cellSampleSize)
balancedSample['cells']['black_male'] = random.sample(genderByRace['cells']['black_male'],cellSampleSize)
balancedSample['cells']['black_female'] = random.sample(genderByRace['cells']['black_female'],cellSampleSize)

balancedSample['factors'] = OrderedDict()

balancedSample['factors']['gender'] = OrderedDict()

balancedSample['factors']['gender']['male'] = []
for row in balancedSample['cells']['white_male']:
    balancedSample['factors']['gender']['male'].append(row)
for row in balancedSample['cells']['black_male']:
    balancedSample['factors']['gender']['male'].append(row)
    
balancedSample['factors']['gender']['female'] = []
for row in balancedSample['cells']['white_female']:
    balancedSample['factors']['gender']['female'].append(row)
for row in balancedSample['cells']['black_female']:
    balancedSample['factors']['gender']['female'].append(row)
    
balancedSample['factors']['race'] = OrderedDict()

balancedSample['factors']['race']['white'] = []
for row in balancedSample['cells']['white_male']:
    balancedSample['factors']['race']['white'].append(row)
for row in balancedSample['cells']['white_female']:
    balancedSample['factors']['race']['white'].append(row)

balancedSample['factors']['race']['black'] = []
for row in balancedSample['cells']['black_male']:
    balancedSample['factors']['race']['black'].append(row)
for row in balancedSample['cells']['black_female']:
    balancedSample['factors']['race']['black'].append(row)    
    
balancedSample['gender_by_race'] = []
for row in balancedSample['cells']['black_male']:
    balancedSample['gender_by_race'].append(row)
for row in balancedSample['cells']['black_female']:
    balancedSample['gender_by_race'].append(row)    
for row in balancedSample['cells']['white_male']:
    balancedSample['gender_by_race'].append(row)
for row in balancedSample['cells']['white_female']:
    balancedSample['gender_by_race'].append(row)   
    
alpha = 0.05
getP = True #As you will soon see, it takes a LONG time to calculate p like this

results, dfWithin = TwoWayANOVA(balancedSample, alpha, getP)    
    
header = '\n\n{:<15} {:<20} {:<10} {:<15} {:<15} {:<15}'.format(' ','SS','DF','MS','F','P')
print(header)
for key, data in results.items():
    if key == 'factors':
        for factor, row in data.items():
            tableString ='{:<15} {:<20} {:<10} {:<15} {:<15} {:<15}'.format(
            key,round(row[0]),row[1],round(row[2]),row[3],row[4])
            print(tableString)
        
    if key == 'interaction':
        tableString ='{:<15} {:<20} {:<10} {:<15} {:<15} {:<15}'.format(
        key,round(data[0]),data[1],round(data[2]),round(data[3]),data[4])
        print(tableString)        
    
    if key == 'within(error)':
        tableString ='{:<15} {:<20} {:<10}'.format(
        key,round(row[0]),data[1], round(data[2]))
        print(tableString)     
    
    if key == 'total':
        tableString ='{:<15} {:<20} {:<10}'.format(
        key,round(data[0]),data[1])
        print(tableString)         
    
if getP:
    for key, data in results.items():
        if key == 'factors':
            for factor, row in data.items():
                if row[5] == True or row[5] == 'nan':
                    resultString ='\nFor {}, the results were significant at alpha = {}, where F({},{}) = {} and p = {}.'.format(
                    factor, alpha, row[1],dfWithin,row[3],row[4])
                    print(resultString)
                if row[5] == False:
                    resultString = '\n{} was not significant at alpha = {}.'.format(
                    factor, alpha)
                    print(resultString)
                    
        if key == 'interaction':
            if data[5] == True or row[5] == 'nan':
                resultString ='\nFor {}, the results were significant at alpha = {}, where F({},{}) = {} and p = {}.'.format(
                key, alpha, data[1],dfWithin,data[3],data[4])
                print(resultString)
            if data[5] == False:
                resultString = '\n{} was not significant at alpha = {}.'.format(
                key, alpha)
                print(resultString)
              
    
import matplotlib.pyplot as plt
plt.style.use('bmh')

positions = []
labels = []
means = []
i = 0    
for key, cell in results['cells'].items():
    labels.append(key)
    means.append(cell[0])
    positions.append(i)
    i+=1
    
plt.bar(positions, means, color='grey',width=0.5,align='center',ecolor='black',
        capsize=5)
plt.xlabel('Sample Incomes')
plt.ylabel('Mean Income($)')
plt.title('Mean Incomes for Race and Gender')
plt.xticks(positions, labels)
plt.show()
    
    
    
    
    
    
    
    
    







                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                






















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    