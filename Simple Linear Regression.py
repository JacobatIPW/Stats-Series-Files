# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:51:31 2020

@author: Jacob
"""

import csv
import random
import matplotlib.pyplot as plt

plt.style.use('bmh')

def simple_linear_regression(data):
    sumX = 0
    sumY = 0
    sumXY = 0
    sumXSquared = 0
    sumYSquared = 0
    numMeasurements = len(data)
    x = []
    for row in data:
        x.append(row[0])
        sumX += row[0]
        sumY += row[1]
        sumXY += row[0]*row[1]
        sumXSquared += row[0]**2
        sumYSquared += row[1]**2
        
        #y = b + mx
        #m = slope
        xMin = min(x)
        xMax = max(x)
        
    slope = ((numMeasurements*sumXY) - (sumX*sumY)) / \
            ((numMeasurements*sumXSquared)-(sumX*sumX))

    #b = intercept
    intercept = ((sumXSquared*sumY) - (sumX*sumXY)) / \
                ((numMeasurements*sumXSquared) - (sumX*sumX))
                
    r_squared = round((numMeasurements*sumXY - sumX*sumY)**2 / \
                    ((numMeasurements*sumXSquared - sumX*sumX)*\
                    (numMeasurements*sumYSquared - sumY*sumY)), 4)
        
    minCalcY = intercept + slope*xMin
    maxCalcY = intercept + slope*xMax
    regression_line = [[xMin,minCalcY],[xMax,maxCalcY]]
    
    return regression_line, r_squared, slope, intercept
        
#Example
dataSet = []

with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        if row[6] != 'INCTOT':
            if int(row[6]) != 9999999:
                if int(row[6]) > 5000  and int(row[6]) > 200000:
                    if int(row[1]) > 17 and int(row[1]) < 65:
                        #Age is our x and income is our y
                        dataSet.append([int(row[1]),int(row[6])])
                        
numSubjects = 500
dataSample = random.sample(dataSet, numSubjects)

regression_line, r_squared, slope, intercept = \
    simple_linear_regression(dataSample)
    
print('R Squared:',round(r_squared,4))
print("For each year of age, a person's income changes by", round(slope,4))
print('Our model: y = ',round(intercept,4),'+',round(slope,4),'*x')

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
plt.plot(x_rl, y_rl)
plt.scatter(x,y)

props = dict(boxstyle='round',facecolor='grey',alpha=0.5)
plt.text(xMin,yMax,'R^2 = '+str(r_squared), fontsize=14,
         verticalalignment='top',bbox=props)
plt.xlabel('Age')
plt.ylabel('Income($)')
plt.title('Simple Regression Age by Income')
plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        