# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:13:37 2018

@author: Em'kay
"""
import numpy as np
import matplotlib.pyplot as plt
import queue
import random


def plotter(data, runlength, title = "XvsY", Xaxis = "x", Yaxis= "y"):
    pis = np.linspace(0,runlength,len(data))
    plt.figure(1)
    plt.plot(pis, data)
    plt.title(title)
    plt.xlabel(Xaxis)
    plt.ylabel(Yaxis)
    plt.show()

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
        
def generateTraceFile(Capacity = 50, avgPacketSize = 1000, workload = 0.8, 
                      write = True):
    traffic = 100
    speed = (1-workload)*Capacity
    packetsNum = ((speed*10**6)/avgPacketSize)
    arrival = (traffic*10**6)/packetsNum
    file = open("testfile.txt","w") 
    file.write("avgIntArrT_Fac,avgPackSize_Arr\n")
    packet = np.random.exponential(avgPacketSize, int(packetsNum))
    atime = np.random.exponential(arrival, int(packetsNum))
    
    if write:
        for i in range(len(atime)):
            file.write(str(int(atime[i])) + "," + str(int(packet[i])) + "\n")
        
    temp = np.zeros(avgPacketSize)
    for i in range(avgPacketSize):
        temp[i] = (np.random.exponential(1000))
        
    file.close()
    return np.asarray([atime,packet]).transpose()

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

def addPriority(data, proportion):
    counter = int(proportion*len(data))
    if proportion >= 1:
        priolist = np.ones(len(data))
        
    else:
        priolist = np.zeros(len(data))
        while counter > 0:
            i = random.randint(0, len(data)-1)
            if priolist[i] == 0:
                priolist[i] = 1
                counter -= 1
       
    print( priolist)   
    out = np.zeros((len(data),3))      
    for i in range(len(data)):
        out[i][0] = priolist[i]
        out[i][1] = data[i][0]
        out[i][2] = data[i][1]
    return out

    
def simulator(capacity, workload, filename = "tracefile.txt" , 
              readFile = True, genQlen = True, verbose = True, write = True):        #  Takes link capacity in Mbps
    if readFile:
        data   = extractData(filename)
    else:
        data   = generateTraceFile(capacity, 1000, workload, write)
  
    data = addPriority(data, 0.2)
    QDelay = np.zeros(len(data))    # Queueing delay 
    RTime  = np.zeros(len(data))    # Response time
    ATime  = np.zeros(len(data))    # Arrival time
    PSize  = np.zeros(len(data))    # Packet size   
    QLength = np.zeros(len(data))  
    Queue = queue.PriorityQueue()              
    lastMesTM = 0                   # last message recieved timestamp
    timer = 0
    transTime = 0

    for i in range(len(data)):
        message = data[i]
        ATime[i] = message[1]
        PSize[i] = message[2]
        timer = message[3]
        
        
        
        
        
#        if genQlen:
#            tempMT = lastMesTM
#            j = i
#            while (tempMT + data[j][1]) < timer:
#                tempMT = tempMT + data[j][2]
#                QLength[i] =  QLength[i] + 1
#                j = j+1
#                if (j == len(data)):
#                    break
#            
#        if (lastMesTM + ATime[i]) > timer:
#            QDelay[i] = lastMesTM + ATime[i] - timer
#            timer = lastMesTM + ATime[i]
#            
#        lastMesTM = lastMesTM + ATime[i]
#        transTime = PSize[i]/capacity
#        RTime[i] = QDelay[i] + transTime
#        timer = timer + transTime
        
    #getAverages(QDelay, 10000, False) 
    if(verbose):
        print ("Total running time in s: " + str(timer/10**6))
        print ("Avarage Arrival time (λ) in us: " + str(ATime.mean()))
        print ("Average packet size (μ): " + str(PSize.mean()))
        print ("Average Response time in ms: " + str(RTime.mean()/10**3))
        print ("Average Queueing delay in ms: " + str(QDelay.mean()/10**3))
    
    return QDelay.mean(), QLength

def getWorkloadResults():
    filename = "testfile.txt"
    workload = np.linspace(0.1,1,10)
    capacity = 100  # link capacity in Mbps
    QdelayPWL = [] # average Queue delay per workload (0-100%)
    k = -1
    for workL in workload:
        k = k+1
        if k == 1:
            continue
        print ("iteration " + str(k))
        avrQDelay = np.zeros(100)
        for i in range(100):
            QDelay, LQ= simulator(capacity, workL, filename, False, 
                                  genQlen = False, verbose = False, 
                                  write = False)
            avrQDelay[i] = QDelay
        plotter(avrQDelay, 100, "Queue delay per iteration with load = " + 
                str(workL), "iteration", "Queue delay (us)" )
        QdelayPWL.append(avrQDelay.mean())  
    
    plotter(QdelayPWL, 100, "Queue delay vs Workload", "Workload (%)", 
            "Queue delay (us)" )
    
#getWorkloadResults()
filename = "testfile.txt"
data = extractData(filename)
prio = addPriority(data, 0.4)
#simulator(100, 0.4, filename, False, genQlen = False, verbose = True)
