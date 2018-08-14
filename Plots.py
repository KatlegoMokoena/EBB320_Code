# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 20:58:56 2018

@author: Em'kay
"""
import numpy as np
import matplotlib.pyplot as plt

def fact(num):
    factorial = 1
    if num < 0:
        return -1;
    elif num == 0:
        return 0;
    else:
       for i in range(1,num + 1):
           factorial = factorial*i
       return factorial

Ar = 50000 # lambda
Sr = 65000 # mu
s = 9

# M/M/1
U = np.linspace(0.001,1,100)
W1 =1/(Sr*(1-U))

# M/M/s
Po = 0
p = U*s
for i in range(s):
    if (i == 0): 
        continue
    Po = Po + ((p**i)/fact(i) + ((p**s)/(fact(s)))*((s*Sr)/(s*Sr-Ar)))
Po = 1/Po
Lq =  (Po*Ar*Sr*p**(s+1))/(fact(s-1)*(s*Sr-Ar)**2)
L2 = Lq + p
W2 = L2/Ar

# M/M/inf
W3 = np.ones(U.shape)
W3 = W3*(1/Sr)

plt.figure(1)
plt.title("Utilization vs Response time")
plt.xlabel("Utilzation")
plt.ylabel("Response time")
plt.plot(U, W1, label = "M/M/1")
plt.plot(U, W2, label = "M/M/s")
plt.plot(U, W3, label = "M/M/inf")
plt.legend()
plt.show()

# M/M/1
L1 = U/(1-U)


plt.figure(2)
plt.title("Number of customers vs Utilization")
plt.ylabel("Number of customers")
plt.xlabel("Utilization")
plt.plot(U, L1, label = "M/M/1")
plt.plot(U, L2, label = "M/M/s")
plt.plot(U, U, label = "M/M/inf")
plt.legend()
plt.show()

#question 2

Ar = np.linspace(1,6500,100) # lambda
L1 = Ar/(Sr-Ar)

Po = 0
p = Ar/Sr
for i in range(s):
    if (i == 0): 
        continue
    Po = Po + ((p**i)/fact(i) + ((p**s)/(fact(s)))*((s*Sr)/(s*Sr-Ar)))
Po = 1/Po
Lq =  (Po*Ar*Sr*p**(s+1))/(fact(s-1)*(s*Sr-Ar)**2)
L2 = Lq + p
L3 = p

plt.figure(3)
plt.title("Number of customers vs Throughput")
plt.ylabel("Number of customers")
plt.xlabel("Throughput")

plt.plot(Ar, L1, label = "M/M/1")
plt.plot(Ar, L2, "*", label = "M/M/s")
plt.plot(Ar, L3, label = "M/M/inf")
plt.legend()
plt.show()

