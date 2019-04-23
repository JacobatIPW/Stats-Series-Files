# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:46:53 2019

@author: Jacob
"""

from math import gamma
from decimal import *

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
    
def getPFromF(f, df1, df2):
    from scipy.intergrate import quad
    probability, error = quad(f_probability_distro_function, 0, f,
                              args=((df1, df2)))
    return probability
    
df1s = [1,2,3,4,5,10,16,30,50,75,120]
df2s = [1,2,3,4,5,10,16,30,50,75,120]
x = []
i = 0
while i <= 30:
    if i <= 3:
        i+=0.01
        x.append(round(i,3))
    elif i > 3 and i <=10:
        i+=5
        x.append(round(i,3))
    elif i > 10 and i <= 30:
        i += 5
        x.append(round(i,3))
        
import matplotlib.pyplot as plt
'''
for df1 in df1s:
    for df2 in df2s:
        y = []
        print(df1, df2)
        for f in x:
            p = f_probability_distro_function(f, df1, df2)
            y.append(round(p,3))
        plt.plot(x,y)
'''
y = []
for f in x:
    p = f_probability_distro_function(f, 120, 120)
    y.append(round(p,3))
plt.plot(x,y)    
plt.show()















        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    