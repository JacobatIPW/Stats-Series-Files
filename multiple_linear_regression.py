# -*- coding: utf-8 -*-
"""
Created on Wed Feb 29 13:34:56 2020

@author: Jacob
"""

import math
import scipy.integrate
from decimal import Decimal, getcontext
import csv
import random
import numpy as np

getcontext().prec = 100

def getMean(sample):
    return sum(sample)/len(sample)
    
def getSampleVariance(sample):
    mean = getMean(sample)
    sumOfSquares = 0
    for row in sample:
        sumOfSquares += (row - mean)**2
    return sumOfSquares/(len(sample) - 1)
    
def getSampleSD(sample):
    return getSampleVariance(sample)**0.5
    
def getSampleStandardError(sample):
    return getSampleSD(sample)/(len(sample)**0.5)
    
def getPooledSD(sample1, sample2):
    return ((getSampleVariance(sample1) + getSampleVariance(sample2))/2)**0.5
    
def gamma(z):
    def function(t,z):
        return Decimal(t)**(Decimal(z) - Decimal(1))*(Decimal(math.e)**(Decimal(-t)))
    gam, error = scipy.integrate.quad(function,0,math.inf,args=(z))
    return gam

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
                if int(row[0]) ==df:
                    if float(row[1]) == round(float(t),2):
                        p = float(row[2])
                        break
    return p
        
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

        
def multiple_linear_regression(data, alpha, getP = True, interaction_test = True):
    independents = []
    dependent = []
    observation_count = 0
    numIVs = len(data[0]) - 1
    
    #In a lot of situations, if you have more than two IVs you will be looking 
    # at only specific interation which are relavant to your hypothesis
    # use the following part mostly as a guild on how to do interaction when
    # making your own analysis code
    
    i = 0
    if interaction_test:
        if numIVs == 2:
            for row in data:
                interaction_term = row[1]*row[2]
                data[i].append(interaction_term)
                i += 1
        if numIVs == 3:
            for row in data:
                interaction_term = row[1]*row[2]
                data[i].append(interaction_term)                
                interaction_term = row[1]*row[3]
                data[i].append(interaction_term)        
                interaction_term = row[2]*row[3]
                data[i].append(interaction_term)        
                interaction_term = row[1]*row[2]*row[3]
                data[i].append(interaction_term)
                i += 1
        
    for row in data:
        dependent.append([row[0]])
        independents.append([1])
        for value in row[1:]:
            independents[observation_count].append(value)
        observation_count += 1
        
    independents = np.array(independents)
    dependent = np.array(dependent)
    transposed_independents = np.transpose(independents)
    transposed_by_independents = np.matmul(transposed_independents,independents)
    inverse_transposed_by_independents = np.linalg.inv(transposed_by_independents)
    transposed_by_dependent = np.matmul(transposed_independents, dependent)
    coefficients = np.matmul(inverse_transposed_by_independents,transposed_by_dependent)
    
    #Calculating R squared and F
    fitted_Ys = []
    for row in data:
        fitted_Y = 0
        currentIV = 0
        while currentIV <= numIVs:
            if currentIV == 0:
                fitted_Y += coefficients[currentIV][0]
            else:
                fitted_Y += row[currentIV]*coefficients[currentIV][0]
            currentIV += 1
        fitted_Ys.append(fitted_Y)
    
    SS_total = 0
    SS_regression = 0
    SS_residual = 0
    dependent_mean = np.mean(dependent)
    
    i = 0
    for row in dependent:
        SS_residual += (row[0] - fitted_Ys[i])**2
        SS_regression += (fitted_Ys[i] - dependent_mean)**2
        i += 1
        
    SS_total = SS_residual + SS_regression
    
    R_Squared = SS_regression/SS_total
    
    DoF_regression = len(coefficients) - 1
    DoF_residual = len(data) - len(coefficients)
    
    #Mean square regression
    MS_regression = SS_regression/DoF_regression
    
    #Mean square error
    MS_residual = SS_residual/DoF_residual
    
    #Our F ratio
    F = MS_regression/MS_residual
    
    p_F = 1 - getPFromF(F, DoF_regression, DoF_residual)
    
    model_sig = False
    if p_F < alpha:
        model_sig = True
        
    model_data = []
    intercept = coefficients[0][0]
    model_data.append(['Overall_model', intercept, R_Squared, F, p_F,
                       model_sig, DoF_regression, DoF_residual])

    #Calculating T for each coefficient
    i = 1
    for coefficient in coefficients[1:]:
        SS_fitted = 0
        SS_x = 0
        x = []
        for row in data:
            x.append(row[i])
        x_mean = getMean(x)
        for row in x:
            SS_x += (row - x_mean)**2
        for row in data:
            SS_fitted += (row[0] - (row[i]*coefficient[0] + intercept))**2
        df = len(data) - 2
        
        standard_error_beta = ((SS_fitted/df)**0.5) / \
                              ((SS_x)**0.5)
        
        t = coefficient[0]/standard_error_beta
        
        p = getPFromT(t,df)
        
        significant = False
        if abs(p) < alpha:
            significant = True

        model_data.append([coefficient[0], t, df, p, significant])
        i += 1
        
    return model_data
        
#Example
dataSet = []
with open('usa_00003.csv',newline='') as newFile:
    data = csv.reader(newFile)
    for row in data:
        #if row[6] == 'INCTOT': print(row)
        if row[6] != 'INCTOT':
            if int(row[6]) > 1 and int(row[1]) < 65:
                #We add our y, and then each x
                #
                #Each Observation [income, education, age]
                dataSet.append([int(row[6]), int(row[4]), int(row[1]), int(row[0])])
                
numSubjects = 100
dataSample = random.sample(dataSet, numSubjects)
alpha = 0.05
getP = True
interaction = True

if interaction:
    labels = ['income', 'education', 'age', 'education_by_age', 'es','as','eas']
else:
    labels = ['income', 'education', 'age', 'sex']
        
results = multiple_linear_regression(dataSample, alpha, getP, interaction)

#Output results
if results[0][5]:
    print('Overall Model p:', round(results[0][4],4))
    print('R^2:', round(results[0][2],4))
    print('F:', round(results[0][3],4))
    print('\nThe overall model was significant at alpha = {} where F({},{}) = {} and p = {}.'.format(
          alpha, results[0][6], results[0][7], round(results[0][3],4),round(results[0][4],4)))
else:
    print('The model was not significant as alpha = {}.'.format(alpha))
    print('Overall Model p:', round(results[0][4],4))
    print('R^2:', round(results[0][2],4))
    print('F:', round(results[0][3],4))

i = 1
model_string = '\nModel: '+labels[0]+' = '+str(results[0][1])
for row in results[1:]:
    model_string = model_string + ' + ' + str(row[0])+'*'+labels[i]

    if row[4]:
        print('\nFor {}, it was significant at alpha = {} where T({}) = {} and p = {}, Coefficient = {} .'.format(
              labels[i], alpha, row[2], row[1], row[3], round(row[0])))        
    else:
        print('\nFor {}, it was not significant as alpha = {}'.format(labels[i], alpha))

        print('T({}) = {} p = {} Coefficient = {}'.format(row[2], 
              row[1], row[3], round(row[0])))
    i += 1
print(model_string)
        
        
        
        

















