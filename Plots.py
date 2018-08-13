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

Ar = 20 # lambda
Sr = 65 # mu
s = 9

# M/M/1
U = np.linspace(0,1,100)
W1 =1/(Sr*(1-U))

# M/M/s
Po = 0
p = U*s
for i in range(s):
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
plt.plot(U, W1, label = "M/M/1")
plt.plot(U, W2, label = "M/M/s")
plt.plot(U, W3, label = "M/M/inf")
plt.legend()
plt.show()

# M/M/1
L1 = U/(1-U)


plt.figure(2)
plt.title("Utilization vs number of customers")
plt.plot(U, L1, label = "M/M/1")
plt.plot(U, L2, label = "M/M/s")
plt.plot(U, U, label = "M/M/inf")
plt.show()

