import numpy as np
import random

def genTrace(mean,size,time,mean2):
	counter = 0
	counter2 = 0
	intarrhigh = 0
	intarrlow = 0
	genHigh = []
	genLow = []
	sizelow = []
	sizehigh =[]
	highpriolist = []
	lowpriorlist = []
	while((intarrlow < time * (10**6))):
		low = np.random.exponential(1/(mean2*10**(-6)))
		sizelow.append(int(np.random.exponential(size)))
		counter += 1
		intarrlow += low
		genLow.append(int(low))
		lowpriorlist.append(0)
		
	while((intarrhigh < time * 10**6)):
		high = np.random.exponential(1/(mean*10**(-6)))
		sizehigh.append(int(np.random.exponential(size)))
		counter2 += 1
		intarrhigh += high
		genHigh.append(int(high))
		highpriolist.append(1)
		
	higher = np.mean(genHigh)
	lower = np.mean(genLow)
	lowpacketsize = np.average(sizehigh)
	highpacketsize = np.average(sizelow)
	mulow = 1/lowpacketsize
	muhigh = 1/highpacketsize
	print("Avg Service Rate mu High", muhigh*10**6)
	print("Arrival Rate High")
	print((1/(higher)) * 10**6)
	print("Avg Service Rate mu low", mulow*10**6)
	print("Arrival Rate Low")
	print((1/(lower)) * 10**6)
	
	text_file = open("highpacks.txt", 'w')
    
	text_file.write("avgIntArrT_Fac,avgPackSize_Arr,Priority\n")
    
	for i in range(len(genHigh)):
		text_file.write(str(highpriolist[i]) + "," + str(genHigh[i]) + "," + str(sizehigh[i])   + "\n")
    
	text_file.close()
	
	text_file = open("lowpacks.txt", 'w')
    
	text_file.write("avgIntArrT_Fac,avgPackSize_Arr,Priority\n")
    
	for i in range(len(genLow)):
		text_file.write( str(lowpriorlist[i]) +  "," +str(genLow[i]) + "," + str(sizelow[i])  + "\n")
    
	text_file.close()

def tracemerge():
    fileHigh = open("highpacks.txt", "r")
    fileLow = open("lowpacks.txt", "r")
    outHigh = []
    outLow = []
    
    i = 0;
    for line in fileHigh:
        i= i+1
        if i != 1:
            temp = line.split(',')
            tempIntArray = [int(temp[0]), int(temp[1]), int(temp[2])]
            outHigh.append(tempIntArray)   
        
    fileHigh.close()
    i = 0;
    for line in fileLow:
        i= i+1
        if i != 1:
            temp = line.split(',')
            tempIntArray = [int(temp[0]), int(temp[1]), int(temp[2])]
            outLow.append(tempIntArray)
    fileLow.close() 
    out = []
    test1  = np.zeros(len(outLow))
    test2  = np.zeros(len(outHigh))
    counterL = 0
    counterH = 0
    while(counterL < len(outLow)-1 or counterH < len(outHigh) -1):
        i = random.randint(0, len(outLow)-1)
        if test1[i] == 0:
            out.append(outLow[i])
            test1[i] = 1
            counterL += 1
        i = random.randint(0, len(outHigh)-1)
        if test2[i] == 0:
            out.append(outHigh[i])
            test2[i] = 1
            counterH += 1
    
    file = open("tracefiles.txt", 'w')
    file.write("avgIntArrT_Fac,avgPackSize_Arr,Priority\n")
    for i in out:
        file.write(str(i[0]) + "," + str(i[1])+ "," + str(i[2]) +"\n")
        
    file.close()
    return out
	
def makeTrace(meanH, meanLow, traffic, size):
    genTrace(meanH, meanLow, traffic, size )
    tracemerge()
    
#genTrace(1000,1000,1,500)
#tracemerge()
#	