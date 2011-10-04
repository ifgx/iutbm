#!/bin/env python
# -*- coding: utf-8 -*-

class Object(object):
    def __init__(self,name,weight,value):
        self.name = name
        self.weight = weight
        self.value = value
        self.rapport = value / weight
        

class Case(object):
    def __init__(self):
        self.value = 0
        self.weight = 0
        self.object = []

    def copy(self,case):
        self.value = case.value
        self.weight = case.weight
        self.object = case.object[:]
    
    def addO(self,obj):
        self.value += obj.value
        self.weight += obj.weight
        self.object.append(obj)
    
    def show(self):
        print('value')
        print(self.value)
        print('weight')
        print(self.weight)
        print('Object')
        for i in self.object:
            print(i.name)

def Sort(x):
    return x.weight/x.value


class Bag(object):
    def __init__(self,Lobject,weight):
        self.Lobject = []
        self.Lobject = sorted(Lobject ,key = lambda x : x.rapport)
        self.numObj = len(Lobject)
        self.weight = weight
        self.tab = [[ Case() for j in range(self.weight+1)] for i in range(self.numObj+1)]

    def solve(self):
        for i in xrange(self.numObj+1):
            for j in xrange(self.weight+1):
                if j == 0 or i == 0:
                    self.tab[i][j].value = 0
                    self.tab[i][j].weight = 0
                else:
                    if j - self.tab[i-1][j].weight >=  self.Lobject[i-1].weight:
                        self.tab[i][j].copy(self.tab[i-1][j]) 
                        self.tab[i][j].addO(self.Lobject[i-1])
                    elif self.tab[i-1][j].value <= self.Lobject[i-1].value:
                        self.tab[i][j].addO(self.Lobject[i-1])
                    else:
                        self.tab[i][j].copy(self.tab[i-1][j])
        print('objet')
        for i in self.Lobject:
            print i.name
        print('weight of the bag')
        print(self.weight)
        self.tab[self.numObj][self.weight].show()  

 
                      

        
