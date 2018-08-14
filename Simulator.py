# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:13:37 2018

@author: Em'kay
"""
import numpy as np

def extractData(filename):
    file = open(filename, "r")
    out = []
    i = 0;
    for line in file:
        i= i+1
        if i != 1:
            temp = line.split(',')
            tempIntArray = [int(temp[0]), int(temp[1])]
            out.append(tempIntArray)   
    return out
        


filename = "tracefile.txt"
data   = extractData(filename)
QDelay = np.zeros(len(data)) # Queueing delay 
RTime  = np.zeros(len(data)) # Response time
ATime  = np.zeros(len(data)) # Arrival time
PSize  = np.zeros(len(data)) # Packet size
capacity = 1 # bandwidth in Mbps
lastMesTM = 0 # last message recieved timestamp
timer = 0
counter = 0
transTime = 0

for i in range(len(data)):
    message = data[i]
    ATime[i] = message[0]
    PSize[i] = message[1]
    if (lastMesTM + ATime[i]) > timer:
        QDelay[i] = lastMesTM + ATime[i] - timer
        timer = lastMesTM + ATime[i]
        
    lastMesTM = lastMesTM + ATime[i]
    transTime = PSize[i]/capacity
    RTime[i] = QDelay[i] + transTime
    timer = timer + transTime
    
print (timer)
print (ATime.mean())
print (capacity/PSize.mean())
print (RTime.mean())
print (QDelay.mean())

