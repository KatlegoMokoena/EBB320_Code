# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:13:37 2018

@author: Em'kay
"""
import numpy as np
import matplotlib.pyplot as plt
import Queue
import random
import generation

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
            tempIntArray = [int(temp[0]), int(temp[1]), int(temp[2])]
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
      
    out = np.zeros((len(data),4))      
    for i in range(len(data)):
        out[i][0] = priolist[i]
        out[i][1] = data[i][0]
        out[i][2] = data[i][1]
        out[i][3] = i
    return out

def addAbsArTime(data):      
    out = np.zeros((len(data),4))      
    for i in range(len(data)):
        out[i][0] = data[i][0]
        out[i][1] = data[i][1]
        out[i][2] = data[i][2]
        out[i][3] = i
    return out
    
def simulator(capacity, workload, filename = "tracefile.txt" , 
              readFile = True, genQlen = True, verbose = True, write = True, 
              priorityDis = 1):        #  Takes link capacity in Mbps
    if readFile:
        data   = extractData(filename)
    else:
        data   = generateTraceFile(capacity, 1000, workload, write)
  
    data = addAbsArTime(data)
    QDelay = np.zeros(len(data))    # Queueing delay 
    RTime  = np.zeros(len(data))    # Response time
    ATime  = np.zeros(len(data))    # Arrival time
    PSize  = np.zeros(len(data))    # Packet size 
    sentP  = np.zeros(len(data))    # Packets sent
    QLength = np.zeros(len(data)) 
    sentorder = np.zeros(len(data)) 
    q = Queue.Queue()              
    lastMesTM = 0                   # last message recieved timestamp
    timer = 0
    transTime = 0

    j = 0
    for i in range(len(data)):
        message = data[i]
        ATime[i] = message[1]
        PSize[i] = message[2]
        #timer = message[3]

        if genQlen:
            tempMT = lastMesTM
            if (j < len(data)):
                while (tempMT + data[j][1]) < timer:
                    tempMT = tempMT + data[j][1]
                    j = j+1
                    if (j == len(data)):
                        break
                    if sentP[j] == 0:
                        q.add([data[j][0], data[j]])
                
            QLength[i] =  q.length()
        sentPacket = q.pop()
        if sentPacket == None:
            k = i
            
        else:
            k = int(sentPacket[1][3])
            if sentPacket[1][2] < timer:
                QDelay[k] = timer - sentPacket[1][2] 
        sentP[k] = 1
        if (k % 10000 == 0):
            print( "sentPacket " + str(k))
        sentorder[k] = i
        
#        if (lastMesTM + ATime[k]) > timer:
#            QDelay[k] = lastMesTM + ATime[k] - timer
#            timer = lastMesTM + ATime[k]
        
            
            
        lastMesTM = lastMesTM + ATime[k]
        transTime = PSize[k]/capacity
        RTime[i] = QDelay[k] + transTime
        timer = timer + transTime
        
    #getAverages(QDelay, 10000, False) 
    if(verbose):
        print ("Total running time in s: " + str(timer/10**6))
        print ("Avarage Arrival time (λ) in us: " + str(ATime.mean()))
        print ("Average packet size (μ): " + str(PSize.mean()))
        print ("Average Response time in ms: " + str(RTime.mean()/10**3))
        print ("Average Queueing delay in ms: " + str(QDelay.mean()/10**3))
    
    return QDelay.mean(), QLength ,data, sentorder

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
filename = "tracefiles.txt"
#data = extractData(filename)
#prio = addPriority(data, 0.5)
#simulator(100, 0.4, filename, False, genQlen = False, verbose = True)
qlen = []
qdelay = []
dataS = None
for i in range(20):
    print ("iteration : " + str(i))
    if i == 0:
        continue
    generation.makeTrace(1000,1000,1,500)
    QDelay, QLength ,dataS, sentorder = simulator(1,1,filename,  verbose = False)
    qlen.append(QLength.mean())
    qdelay.append(QDelay)
    
plotter(qdelay, 100, "DDD", "DDDs","DDDCC")
