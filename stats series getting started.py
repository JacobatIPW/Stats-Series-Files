# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 06:31:40 2018

@author: Jacob
"""

import csv
print('I worked!')
i = 0
with open('usa_00003.csv', newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        print(i, row)
        i+=1
        if i > 100:
            break
        