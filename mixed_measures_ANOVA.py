# -*- coding: utf-8 -*-
"""
Created on Mon Jan 6 15:02:22 2019

@author: Jacob
"""

import math
import scipy.integrate
from decimal import *
import csv
import random
from collections import OrderedDict

getcontext().prec = 100

def getMean(sample):
    return sum(sample)/len(sample)
    
def gamma(z):
    def function(t,z):
        e = math.e
        return Decimal(t)**(Decimal(z)-Decimal(1))*(Decimal(e)**(Decimal(-t)))
    gam, error = scipy.integrate.quad(function,0,math.inf,args=(z))
    return gam
    
def f_probability_distro_function(f,df1,df2):
    top = ((Decimal(df1)*Decimal(f))**Decimal(df1))*(Decimal(df2)**Decimal(df2))
    bottom = (Decimal(df1)*Decimal(f)+Decimal(df2))**(Decimal(df1)+Decimal(df2))
    num = (Decimal(top)/Decimal(bottom))**Decimal(0.5)
    a = df1/2
    b = df2/2
    try:
        beta = (math.gamma(a)*math.gamma(b))/math.gamma(a+b)
    except OverflowError:
        beta = (gamma(a)*gamma(b))/gamma(a+b)
    if f == 0: f = 0.0000000001
    denom=f*beta
    pdf= float(num)/float(denom)
    return pdf
    
def getPFromF(f, df1, df2):
    p,error = scipy.integrate.quad(f_probability_distro_function,0,f,
                                   args=((df1,df2)))
    return p
    
#new stuff
def mixed_measures_two_way_ANOVA(data,alpha,getP=False):
    #dof = degrees of freedom
    #IF = independent factor
    #DF = dependent factor
    dof_IF = len(data) - 1
    #I need the key and nested values to get the number of subject per cell
    #I also get the number of DF levels here
    IFKey, IFNestedValues = next(iter(data.items()))
    numSubjectsPerCell = len(next(iter(IFNestedValues.values())))
    #The error DoF of the IF is the number of levels of the IF times the cell size
    #minus 1
    dof_IF_Error = len(data)*(numSubjectsPerCell - 1)
    dof_DF = len(IFNestedValues) - 1
    #DoF of the interaction
    dof_Interaction = (len(data) - 1)*(len(IFNestedValues)-1)
    #dof of the Interaction and DF
    dof_DF_Interaction_Error = len(data)*(len(IFNestedValues) - 1)*(numSubjectsPerCell - 1)
    #The Number of Measurements
    numMeasurements = len(data)*len(IFNestedValues)*numSubjectsPerCell
    dof_Total = numMeasurements - 1
    
    #Sum of Squares (SS) for the independent factor
    #The SS IF is the sum of each level of the IF squared
    #divided by the number of DF levels times the cell size all minus th
    #sum of all measurements squared divided by the total measurements
    eachIFLevelSummedSquared = []
    sumOfEachMeasurement = 0
    for level, levelValues in data.items():
        iFSquared = 0
        for levels, dependentValues in levelValues.items():
            for row in dependentValues:
                iFSquared += row
                sumOfEachMeasurement += row
        eachIFLevelSummedSquared.append(iFSquared**2)
    sumOfEachMeasurementSquared = sumOfEachMeasurement**2
    sumOfEachIFLevelSummedSquared = sum(eachIFLevelSummedSquared)
    
    SS_IF = (sumOfEachIFLevelSummedSquared/(len(IFNestedValues)*numSubjectsPerCell)) - \
    (sumOfEachMeasurementSquared/numMeasurements)
    
    #MS = mean square
    #The MS is the SS divided by the dof
    MS_IF = SS_IF/dof_IF
    print(SS_IF,dof_IF)
    #SS of the Error of the IF
    currentIF = 0
    eachParticipantSummed = []
    for i in range(len(data)*numSubjectsPerCell):
        eachParticipantSummed.append(0)
    
    for level, levelValues in data.items():
        for levels,dependentValues in levelValues.items():
            participantInDF = numSubjectsPerCell*currentIF
            for row in dependentValues:
                eachParticipantSummed[participantInDF] += row
                participantInDF += 1
        currentIF += 1
        
    eachParticipantSummedSquared = []
    for row in eachParticipantSummed:
        eachParticipantSummedSquared.append(row**2)
        
    sumOfEachParticipantSummedSquared = sum(eachParticipantSummedSquared)
    
    SS_IF_Error = (sumOfEachParticipantSummedSquared/len(IFNestedValues)) - \
    (sumOfEachIFLevelSummedSquared/(len(IFNestedValues)*numSubjectsPerCell))
    
    MS_IF_Error = SS_IF_Error/dof_IF_Error
    
    #The f ratio is the mean square divided by the mean square of the error
    F_IF = MS_IF/MS_IF_Error
    #SS of the DF
    eachDFLevelSummed = []
    for level, levelValues in data.items():
        currentDFLevel = 0
        for levels, dependentValues in levelValues.items():
            if len(eachDFLevelSummed) < 1:
                for i in range(len(IFNestedValues)):
                    eachDFLevelSummed.append(0)
            for row in dependentValues:
                eachDFLevelSummed[currentDFLevel] += row
            currentDFLevel += 1
            
    eachDFLevelSummedSquared = []
    for row in eachDFLevelSummed:
        eachDFLevelSummedSquared.append(row**2)
        
    sumOfEachDFLevelSummedSquared = sum(eachDFLevelSummedSquared)
    
    SS_DF = (sumOfEachDFLevelSummedSquared/(len(data)*numSubjectsPerCell)) - \
    (sumOfEachMeasurementSquared/numMeasurements)
    
    MS_DF = SS_DF/dof_DF
    
    #SS Interaction (skipping SS for the DF Error for now)
    eachCellSummedSquared = []
    for level, levelValues in data.items():
        for levels, dependentValues in levelValues.items():
            cellTotal = 0
            for row in dependentValues:
                cellTotal += row
            eachCellSummedSquared.append(cellTotal**2)
    sumOfEachCellSummedSquared = sum(eachCellSummedSquared)
    
    SS_Interaction = (sumOfEachCellSummedSquared/numSubjectsPerCell) - \
    (sumOfEachIFLevelSummedSquared/(len(IFNestedValues)*numSubjectsPerCell)) - \
    (sumOfEachDFLevelSummedSquared/(len(data)*numSubjectsPerCell)) + \
    (sumOfEachMeasurementSquared/numMeasurements)
    
    MS_Interaction = SS_Interaction/dof_Interaction
    #SS Total
    eachMeasurementSquared = 0
    for level, levelValues in data.items():
        for levels, dependentValues in levelValues.items():
            for row in dependentValues:
                eachMeasurementSquared += row**2
    SS_Total = eachMeasurementSquared - (sumOfEachMeasurementSquared/numMeasurements)
    
    SS_DF_Interaction_Error = SS_Total - SS_Interaction - SS_DF - SS_IF_Error - SS_IF
    if SS_DF_Interaction_Error == 0: SS_DF_Interaction_Error = 0.00000001
    MS_DF_Interaction_Error = SS_DF_Interaction_Error/dof_DF_Interaction_Error
    
    #Now we can get to the last two f ratios
    F_DF = MS_DF/MS_DF_Interaction_Error
    F_Interaction = MS_Interaction/MS_DF_Interaction_Error
    
    sig_IF = False
    sig_DF =False
    sig_Interaction = False
    
    if getP:
        print('calculating p values')
        p_IF = 1 - getPFromF(F_IF, dof_IF, dof_IF_Error)
        p_DF = 1 - getPFromF(F_DF, dof_DF, dof_DF_Interaction_Error)
        p_Interaction = 1 - getPFromF(F_Interaction, dof_Interaction, 
                                      dof_DF_Interaction_Error)
        p_IF = round(p_IF,4)
        p_DF = round(p_DF,4)
        p_Interaction = round(p_Interaction,4)
        print('p_IF',p_IF)
        print('p_DF',p_DF)
        print('p_Interaction',p_Interaction)
        if p_IF < alpha:
            sig_IF = True
        if p_DF < alpha:
            sig_DF = True            
        if p_Interaction < alpha:
            sig_Interaction = True    
    
    else:
        p_IF = 'N/A'
        p_DF = 'N/A'
        p_Interaction = 'N/A'
    
    modelTable = OrderedDict()
    
    modelTable['IF'] = [SS_IF, dof_IF, MS_IF, F_IF, p_IF, sig_IF]
    modelTable['IF Error'] = [SS_IF_Error, dof_IF_Error, MS_IF_Error]
    modelTable['DF'] = [SS_DF, dof_DF, MS_DF, F_DF, p_DF, sig_DF]
    modelTable['Interaction'] = [SS_Interaction, dof_Interaction, MS_Interaction,
                                F_Interaction, p_Interaction, sig_Interaction]
    modelTable['DF Int Err'] =[SS_DF_Interaction_Error, dof_DF_Interaction_Error,
                                MS_DF_Interaction_Error]
    modelTable['Total'] = [SS_Total, dof_Total]
    
    return modelTable, dof_IF_Error, dof_DF_Interaction_Error
    
    
#Now for our example
dataSet = OrderedDict()
dataSet['male'] = []
dataSet['female'] = []

with open('usa_00003.csv',newline='') as newFile:
    data =  csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) != 9999999:
                if int(row[6]) > 5000 and int(row[6]) < 200000:
                    if int(row[1]) > 17:
                        if int(row[0]) == 1:
                            dataSet['male'].append(int(row[6]))
                        if int(row[0]) == 2:
                            dataSet['female'].append(int(row[6]))
numSubjects = 50
minBonus = 0
maxBonus = 1000
dataSample = OrderedDict()

dataSample['male'] = OrderedDict()
dataSample['male']['before'] = random.sample(dataSet['male'], numSubjects)

dataSample['male']['oneClass'] = []
for row in dataSample['male']['before']:
    oneClass = row + random.randint(minBonus, maxBonus)
    dataSample['male']['oneClass'].append(oneClass)
        
dataSample['male']['twoClasses'] = []
for row in dataSample['male']['oneClass']:
    twoClasses = row + random.randint(minBonus, maxBonus)
    dataSample['male']['twoClasses'].append(twoClasses)        
        
dataSample['male']['threeClasses'] = []
for row in dataSample['male']['twoClasses']:
    threeClasses = row + random.randint(minBonus, maxBonus)
    dataSample['male']['threeClasses'].append(threeClasses)        
        
dataSample['female'] = OrderedDict()
dataSample['female']['before'] = random.sample(dataSet['female'], numSubjects)

dataSample['female']['oneClass'] = []
for row in dataSample['female']['before']:
    oneClass = row + random.randint(minBonus, maxBonus)
    dataSample['female']['oneClass'].append(oneClass)
        
dataSample['female']['twoClasses'] = []
for row in dataSample['female']['oneClass']:
    twoClasses = row + random.randint(minBonus, maxBonus)
    dataSample['female']['twoClasses'].append(twoClasses)        
        
dataSample['female']['threeClasses'] = []
for row in dataSample['female']['twoClasses']:
    threeClasses = row + random.randint(minBonus, maxBonus)
    dataSample['female']['threeClasses'].append(threeClasses)         
        
#The gives us a sample with an IF with two levels and a DF with 4 levels

alpha = 0.05
getP = True

results, dof_IF_Error, dof_DF_Interaction_Error = \
mixed_measures_two_way_ANOVA(dataSample, alpha, getP)        
        
header = '\n\n{:<15}{:<15}{:<6}{:<15}{:<10}{:<10}'.format('','SS','DF','MS','F','P')
print(header)

for key, data in results.items():
    if key == 'IF':
        tableString = '{:<15}{:<15}{:<6}{:<15}{:<10}{:<10}'.format(key, round(data[0]),
        data[1],round(data[2]),round(data[3],4),data[4])
        print(tableString)
    if key == 'IF Error':
        tableString = '{:<15}{:<15}{:<6}{:<15}'.format(key, round(data[0]),
        data[1],round(data[2]))
        print(tableString)        
    if key == 'DF':
        tableString = '{:<15}{:<15}{:<6}{:<15}{:<10}{:<10}'.format(key, round(data[0]),
        data[1],round(data[2]),round(data[3],4),data[4])
        print(tableString)        
    if key == 'Interaction':
        tableString = '{:<15}{:<15}{:<6}{:<15}{:<10}{:<10}'.format(key, round(data[0]),
        data[1],round(data[2]),round(data[3],4),data[4])
        print(tableString)        
    if key == 'DF Int Err':
        tableString = '{:<15}{:<15}{:<6}{:<15}'.format(key, round(data[0]),
        data[1],round(data[2]))
        print(tableString)         
    if key == 'Total':
        tableString = '{:<15}{:<15}{:<6}'.format(key, round(data[0]),
        data[1])
        print(tableString)         
if getP:
    for key, data in results.items():
        if key == 'IF':
            if data[5] ==True:
                resultString = '\nFor the IF, the results were significant at'+\
                'alpha = {}, where F({},{}) = {} and p = {}'.format(alpha, data[1],
                dof_IF_Error, data[3], round(data[4],4))
                print(resultString)
            else:
                resultString = '\nFor DF, the results were not significant at alpha ={}'.format(
                alpha)
        if key == 'DF':
            if data[5] ==True:            
                resultString = '\nFor the DF, the results were significant at'+\
                'alpha = {}, where F({},{}) = {} and p = {}'.format(alpha, data[1],
                dof_IF_Error, data[3], round(data[4],4))
                print(resultString)
            else:
                resultString = '\nFor Interaction, the results were not significant at alpha ={}'.format(
                alpha)
        if key == 'Interaction':
            if data[5] ==True:            
                resultString = '\nFor the Interaction, the results were significant at'+\
                'alpha = {}, where F({},{}) = {} and p = {}'.format(alpha, data[1],
                dof_IF_Error, data[3], round(data[4],4))
                print(resultString)
            else:
                resultString = '\nFor Interaction, the results were not significant at alpha ={}'.format(
                alpha)
            
import matplotlib.pyplot as plt
plt.style.use('bmh')

positions = []
labels = []
means = []
i = 0

for IFKey, IFLevel in dataSample.items():
    for DFKey, dfLevel in IFLevel.items():
        labels.append(IFKey+'_'+DFKey)
        means.append(getMean(dfLevel))
        positions.append(i)
        i+=1
        
plt.bar(positions, means, color='grey',width=0.5,align='center',ecolor='black',
        capsize=5)
plt.xlabel('Sample Incomes')
plt.ylabel('Mean Income($)')
plt.title('Mean Incomes for Awesome Make Lots of Money Classes')
plt.xticks(positions,labels, rotation=45)
plt.show()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            















