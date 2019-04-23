# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 12:21:41 2019

@author: Jacob
"""

#Make a graph of the standard normal distribution

x = []
y = []
i = -4
while i<4:
    i+=0.01
    x.append(round(i,3))
    
#Euler's Number
e = 2.718281828459
#pi
pi = 3.14159265
#Constant
c = 1/((2*pi)**0.5)
for a in x:
    #exponent
    expo = (-a**2)/2
    #distrobution formula
    distro = c*(e**expo)
    y.append(distro)
    
import matplotlib.pyplot as plt
plt.plot(x,y)
#plt.show()
    
import scipy.integrate
#Docs:
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html
#If there is an error, update your modules using pip

#lower limit
negative_infinity = -float('inf')
#Upper limit
z = 0
#Function of x
def f(x):
    #constant
    c = 1/((2*pi)**0.5)
    exponent = (-x**2)/2
    standard_normal_curve = c*(e**exponent)
    return standard_normal_curve
    
probability, error = scipy.integrate.quad(f, negative_infinity, z)

print(round(probability,5))


z_table = []

for row in x:
    probability, error = scipy.integrate.quad(f, negative_infinity, row)
    z_table.append([row,round(probability,5)])
    #print(row, round(probability,5))
    
import csv
with open('z_table.csv', 'w',newline='') as zTableFile:
    z_table_writer = csv.writer(zTableFile,delimiter=',')
    for row in z_table:
        z_table_writer.writerow(row)
        
        
    































 
    
    
    
    
    
    
    
    
    
    
    