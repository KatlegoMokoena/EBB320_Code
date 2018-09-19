# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 23:35:48 2018

@author: Em'kay
"""

class Queue():
    data = []
    
    def Queue(self):
        self.data = []
        
    def add(self, inputdata):
        self.data.append(inputdata)
    
    def pop(self):
        low = -1
        res = 0
        for i in range(len(self.data)):
            if self.data[i][0] > low and self.data[i][0] != -1:
                res = i
                low = self.data[i][0] 
        
        if low == -1:
            return None
        
        ret  = self.data[res]
        self.data[res][0] = -1
        return ret
    
