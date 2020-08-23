# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:49:41 2020

@author: Jacob
"""

import math
import scipy.integrate
from decimal import Decimal, getcontext
import csv
import random
import matplotlib.pyplot as plt

plt.style.use('bmh')
getcontext().prec = 100

def getMean(sample):
    return sum(sample)/len(sample)
    
def gamma(z):
    def function(t,z):
        e = math.e
        return Decimal(t)**(Decimal(z)-Decimal(1))*(Decimal(e)**(Decimal(-t)))
    gam, error = scipy.integrate.quad(function,0,math.inf,args=(z))
    
def f_probability_distro_function(f,df1,df2):
    num = (((Decimal(df1)*Decimal(f))**Decimal(df1))*(Decimal(df2)**Decimal(df2)) / \
           (Decimal(df1)*Decimal(f)+Decimal(df2))**(Decimal(df1)+Decimal(df2)))**Decimal(0.5)
    
    a = df1/2
    b = df2/2
    try:
        beta = (math.gamma(a)*math.gamma(b))/math.gamma(a+b)
    except OverflowError:
        beta = (gamma(a)*gamma(b))/gamma(a+b)
    if f == 0: f = 0.000000001
    denom = f*beta
    pdf = float(num)/float(denom)
    return pdf
    
def getPFromF(f, df1, df2):
    p,error = scipy.integrate.quad(f_probability_distro_function, 0, f,
                                   args=((df1,df2)))
    return p
    
def simple_linear_regression(data, alpha, getP = True):
    sumX = 0
    sumY = 0
    sumXY = 0
    sumXSquared = 0
    sumYSquared = 0
    numMeasurements = len(data)
    x=[]
    y=[]
    
    for row in data:
        x.append(row[0])
        y.append(row[1])
        sumX +=row[0]
        sumY += row[1]
        sumXY += row[0]*row[1]
        sumXSquared += row[0]**2
        sumYSquared += row[1]**2
        
    xMin = min(x)
    xMax = max(x)
    
    slope = ((numMeasurements*sumXY) - (sumX*sumY)) / \
            ((numMeasurements*sumXSquared) - (sumX*sumX))
    
    intercept = ((sumXSquared*sumY) - (sumX*sumXY)) / \
                ((numMeasurements*sumXSquared) - (sumX*sumX))    
    
    r_squared = round((numMeasurements*sumXY - sumX*sumY)**2 / \
                ((numMeasurements*sumXSquared - sumX*sumX)*\
                 (numMeasurements*sumYSquared - sumY*sumY)),4)
    
    minCalcY = intercept + slope*xMin
    maxCalcY = intercept + slope*xMax
    
    regression_line = [[xMin, minCalcY],[xMax,maxCalcY]]
    
    #We need to build the sum of squares for the error of the fitted model and 
    #the sum of squares error for the reduced model
    #The reduced model is just the intercept without our IV
    
    #SSEF is the Sum of Squares Error of the fitted model
    #SSER is the Sum of Squares Error of the reduced model
    
    SSEF = 0
    SSER = 0
    
    for row in data:
        fittedY = intercept + slope*row[0]
        reducedY = intercept
        
        SSEF += (row[1] - fittedY)**2
        SSER += (row[1] - reducedY)**2
                 
    #Degress of freedom for the reduced model
    dof_r = len(data) - 1
    #Degrees of freedom for the full model
    dof_f = len(data) - 2
    dof_factors = len(data[0]) - 1
                    
    F = round(((SSER - SSEF)/(dof_r - dof_f)) / \
        (SSEF/dof_f),4)
    
    significance = False
    if getP:
        p = round(1 - getPFromF(F, dof_factors, dof_f),6)
        if p < alpha: significance = True
    else:
        p = 'N/A'
    
    return regression_line, r_squared, slope, intercept, \
            F, p, significance, dof_factors, dof_f
            
#Example
dataSet = []
with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) != 9999999:
                if int(row[6]) > 1:
                    #Education is our x and income is our y
                    dataSet.append([int(row[4]), int(row[6])])
numSubjects = 300
dataSample = random.sample(dataSet, numSubjects)
alpha = 0.05
getP = True

regression_line, r_squared, slope, intercept, F, p, significance, dof_factors, dof_f = \
simple_linear_regression(dataSample, alpha, getP)
    
#Output results
if significance:
    print('R^2:', r_squared)
    print('p:',p)
    print('F:',F)
    print("For each level of education, a person's income changes by", round(slope,4))
    print('Our model: y = {} + {}x'.format(round(intercept,4),round(slope,4)))
    print('\nThe model was significant at alpha = {} where F({},{}) ={} and p ={}.'.format(
          alpha, dof_factors, dof_f, F, p))
else:
    print('The model was not significant as alpha ={}.'.format(alpha))
    print('R^2:', r_squared)
    print('p:',p)
    print('F:',F)        
    
x_rl = []
y_rl = []
x = []
y = []
for row in regression_line:
    x_rl.append(row[0])
    y_rl.append(row[1])

for row in dataSample:
    x.append(row[0])
    y.append(row[1])

xMin = min(x)
yMax = max(y)
    
plt.plot(x_rl,y_rl)
plt.scatter(x,y)

props = dict(boxstyle='round',facecolor='grey',alpha=0.5)
plt.text(xMin,yMax,'R^2='+str(r_squared), fontsize=14,
         verticalalignment='top',bbox=props)
plt.xlabel('Education')
plt.ylabel('Income ($)')
plt.title('Simple Regression of Education by Income')
plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    