# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 06:12:36 2019

@author: Jacob
"""

import csv
#i = 0
#List to hold sub sample
data_list = []
with open('usa_00003.csv', newline='') as myFile:
    data = csv.reader(myFile)
    for row in data:
        #i+=1
        data_list.append(row)
        #size of our sample
        #if i > 30000:
        #   break
#The average calculation:
#Sum all of the data points of a varible
# and divide by the number of points
print(data_list[0])
#   0      1      2        3       4        5        6
#['SEX', 'AGE', 'RACE', 'RACED', 'EDUC', 'EDUCD', 'INCTOT']         
sumTotal = 0
sampleSize = 0
for row in data_list[1:]:
    if int(row[6]) != 9999999:
        sumTotal = int(row[6])+sumTotal
        sampleSize +=1
    #print(row)
average = sumTotal/sampleSize
print('Mean:',average)
#average income = 1707201.1985333334 ---Is this correct?
#No!
#34690.20 --- More realistic!


#Mode
#How the race variable is coded:
white = 0 #1
black = 0 #2
americian_indian = 0 #3
chinese = 0 #4
japanese = 0#5
other_asian = 0#6
other_race = 0#7
two_races = 0#8
three_races = 0#9

for row in data_list[1:]:
    if row[2] == '1':
        white +=1
    if row[2] == '2':
        black +=1
    if row[2] == '3':
        americian_indian +=1
    if row[2] == '4':
        chinese +=1
    if row[2] == '5':
        japanese +=1
    if row[2] == '6':
        other_asian +=1
    if row[2] == '7':
        other_race +=1
    if row[2] == '8':
        two_races +=1
    if row[2] == '9':
        three_races +=1
mode = max(white,black,americian_indian,chinese,japanese,other_asian,other_race,two_races, three_races)
print('Race counts: ', white,black,americian_indian,chinese,japanese,other_asian,other_race,two_races, three_races)
print('Mode:',mode)

#median
medianEdu = 0
def takeFith(elem):
    return elem[4]
data_list.sort(key=takeFith)
sampleSize = len(data_list)
middle = sampleSize/2
medianEdu = data_list[int(round(middle))]
print('median Education: ', medianEdu[4])
#06 is grade 12

medianIncome = 0
def takeSixth(elem):
    return elem[5]
data_list.sort(key=takeSixth)
sampleSize = len(data_list)
middle = sampleSize/2
medianIncome = data_list[int(round(middle))]
print('Median Income: ', medianIncome)

#Range

cleanedIncome = []
for row in data_list[1:]:
    if row[6] != 'INCTOT':
        if int(row[6]) != 9999999:
            cleanedIncome.append(int(row[6]))
        
minIncome = min(cleanedIncome)
maxIncome = max(cleanedIncome)
print('Min Income: ', minIncome, 'Max Income: ', maxIncome)
#Min Income:  -5800 Max Income:  731000







































        