import numpy as np
import csv
import math

dhParams = []   #defining matrix to store dh parameters

#----------reading data from the file-----------------
with open('dhParametersInputs.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        singelRow = [float(row['Alpha']), float(row['A']), float(row['D']), float(row['Theeta']), row['Range']]
        dhParams.append(singelRow)

m = len(dhParams)   #number of Joints

i = 1;  #loop variable
#setting print options of numpy
np.set_printoptions(formatter={'float': '{: 0.4f}'.format})

for val in dhParams:
    #Formula for (i-1)T(i)
    # T = (c0     -s0     O       A)
    #     s0calp  c0calp  -salp   -salpD
    #     s0salp  c0salp  calp    calpD
    #     0       0       0       1
    #defining (i-1)T(i) matrix
    T = np.matrix( [[math.cos(math.radians(val[3])), -1*math.sin(math.radians(val[3])), 0, val[1] ],\
    [  math.sin(math.radians(val[3]))*math.cos(math.radians(val[0])), math.cos(math.radians(val[3]))*math.cos(math.radians(val[0])), -1*math.sin(math.radians(val[0])), -1*math.sin(math.radians(val[0])) * val[2]   ],\
    [  math.sin(math.radians(val[3]))*math.sin(math.radians(val[0])), math.cos(math.radians(val[3]))*math.sin(math.radians(val[0])),  math.cos(math.radians(val[0])), math.cos(math.radians(val[0])) * val[2]  ],\
    [0,0,0,1]] )
    print("\n ("+str(i-1)+')T('+str(i)+') == ')
    print(T)
    if 1==i:
        B = T
    else:
        B = B*T     #Post Multiplication for finding the end matrix
    i+=1

print("\n"+'(0)T(m) == (0)T('+str(m)+ ') ==')
print(B)   #Printing manipulator transformation matrix

#Formula on P43 - indexing from zero
#beta = ATan2(-r20, sqrt(r00^2,r10^2))
#alpha = ATan2(r10/cosBeta, r00/cosBeta)
#gamma = ATan2(r21/cosBeta, r22/cosBeta)
cosB = math.sqrt(B.item(0,0)*B.item(0,0) + B.item(1,0)*B.item(1,0))
beta = math.atan2(-B.item(2,0), cosB)
alpha = math.atan2(B.item(1,0)/cosB, B.item(0,0)/cosB)
gamma = math.atan2(B.item(2,1)/cosB, B.item(2,2)/cosB)

print('\n\n Final Cartesian space cordinates relative to base = (0)P == '+str([round(B.item(0,3),3), round(B.item(1,3),3), round(B.item(2,3),3)]))
print('\n\n X-Y-Z fixed angles in degrees:')
print(" Gamma = "+str(math.degrees(gamma)))
print(" Beta = "+str(math.degrees(beta)))
print(" Alpha = "+str(math.degrees(alpha)))
