# -*- coding: utf-8 -*-
"""
Created on Sat May  6 12:14:18 2019

@author: Jacob
"""

import math
import scipy.integrate

#The standard normal distribution probability density function
def snd_pdf(x):
    pdf = (1/((2*math.pi)**0.5))*(math.e**(-0.5*(x**2)))
    return pdf
#Standard normal sidtribution cumulative distribution function
def snd_cdf(x):
    return (1+math.erf(x/2**0.5))/2
    
#Studentized range distribution cumulative distribution function
#k = numGroups
#v = df
def srd_cdf_poly_two(q, df, numGroups):
    def f(x, q, df, numGroups):
        func1 = (x**(df-1))*math.e**(-(df*x**2)/2)#Check
        def subPolyTwo(u,x, q, numGroups):
            subPoly = snd_pdf(u)*(snd_cdf(u) - snd_cdf(u-q*x))**(numGroups-1)
            return subPoly
        func2, error = scipy.integrate.quad(subPolyTwo, -math.inf,
                                            math.inf,args=(x, q, numGroups))
        func = func1*func2
        return func
    polyTwo, error = scipy.integrate.quad(f, 0, math.inf,
                                          args=(q, df, numGroups))
    return polyTwo

def srd_cdf(q,numGroups, df):
    polyOne = (numGroups*df**(df/2))/(math.gamma(df/2)*2**(df/2-1))
    polyTwo = srd_cdf_poly_two(q, df, numGroups)
    p = polyOne*polyTwo
    return p
    
q = 3.889
df = 30
numGroups = 2

print(round(1-srd_cdf(q, numGroups, df), 3))    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




















