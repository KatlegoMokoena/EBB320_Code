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
    file.close() 
    return out
        
def generateTraceFile(Capacity = 50, avgPacketSize = 1000):
    servRate = ((Capacity*10**6)/avgPacketSize)*100
    print (int(servRate))
    file = open("testfile.txt","w") 
    #test = np.random.exponential(1000*Capacity, 100000)
    test = np.random.exponential(1000, int(servRate))
    test2 = np.random.exponential(1000, int(servRate))
    
    for i in range(len(test)):
        file.write(str(int(test2[i])) + "," + str(int(test[i])) + "\n")
        
    temp = np.zeros(avgPacketSize)
    for i in range(avgPacketSize):
        temp[i] = (np.random.exponential(1000))
        
    file.close()
    print (test.mean())
    return test

def getAverages(Qdelay, increment = 10000, verbose = True):
    temp = []    
    av = []
    counter = 0
    if verbose:
        print ("-----------------------------------")
    for i in range(len(Qdelay)):
        temp.append(Qdelay[i])
        counter = counter + 1
        if counter == increment:
            counter = 0;
            tempArr = np.asarray(temp)
            avv = tempArr.mean();
            if verbose:
                print("Average is: " + str("{0:.4f}".format(avv)) + " " + str(i+1))
            av.append(avv)
     
    if verbose:
        print ("-----------------------------------")
    return np.asarray(av)

def simulator(capacity = 1):        #  Takes link capacity in Mbps
    filename = "testfile.txt"
    #filename = "tracefile.txt"
    data   = extractData(filename)
    QDelay = np.zeros(len(data))    # Queueing delay 
    RTime  = np.zeros(len(data))    # Response time
    ATime  = np.zeros(len(data))    # Arrival time
    PSize  = np.zeros(len(data))    # Packet size                   
    lastMesTM = 0                   # last message recieved timestamp
    timer = 0
    transTime = 0
    capacity = 1
    
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
        
    getAverages(QDelay, 10000, False)
    print ("Total running time in us: " + str(timer))
    print ("Avarage Arrival time (λ) in us: " + str(ATime.mean()))
    print (PSize.mean())
    print ("Average packet size (μ): " + str((capacity*(10**6))/PSize.mean()))
    print ("Average Response time in us: " + str(RTime.mean()))
    print ("Average Queueing delay in us: " + str(QDelay.mean()))

capacity = 5   # link capacity in Mbps
test = generateTraceFile(capacity)
simulator(capacity)
