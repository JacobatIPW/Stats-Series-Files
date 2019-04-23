# -*- coding: utf-8 -*-
"""
Created on Sat Feb  11 06:25:11 2019

@author: Jacob
"""

pi = 3.14159265

x = []
i = -6
while i < 6:
    i+=0.01
    x.append(round(i,3))
    
from math import gamma

def numerator(df):
    n = (df+1)/2
    num = gamma(n)
    return num
    
def denominator(df):
    pi = 3.14159265
    n = df/2
    x = (df*pi)**0.5
    gam = gamma(n)
    denom = x*gam
    return denom
    
def poly(t,df):
    x = (1+((t**2)/df))
    expo = -((df+1)/2)
    polynom = x**expo
    return polynom
    
def t_probability_distro_function(t,df):
    num = numerator(df)
    denom = denominator(df)
    polynom = poly(t,df)
    pdf = (num/denom)*polynom
    return pdf
    
import scipy.integrate

negative_infinity = -float('inf')
df = 1
t_table = []

while df <= 120:
    for row in x:
        probability, error = scipy.integrate.quad(t_probability_distro_function,
                                                  negative_infinity, row,
                                                  args=(df))
        t_table.append([df, row, round(probability,5)])
    df+=1
    
import csv
with open('t_table.csv','w',newline='') as tTableFile:
    tTableWriter = csv.writer(tTableFile,delimiter=',')
    for row in t_table:
        tTableWriter.writerow(row)
        
import matplotlib.pyplot as plt

df = 1
while df <= 120:
    y = []
    for row in x:
        pdf = t_probability_distro_function(row, df)
        y.append(pdf)
    plt.plot(x,y)
    df+=1
plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    