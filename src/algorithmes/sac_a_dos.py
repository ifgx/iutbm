#!/bin/env python
# -*- coding: utf-8 -*-


class Object(object):
    '''
        the class Object allow you to create object with a name, a value, and a weight
    '''

    def __init__(self,name,weight,value):
        self.name = name
        self.weight = weight
        self.value = value
        self.rapport = self.value/self.weight


class Case(object):
    '''
        the class Case allow you to create case which are used to solve the Bag problem
    '''
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

class Bag(object):
    '''
        the class bag allow you to create bag who are defined by a list of object and a weight
    '''
    def __init__(self,Lobject,weight):
        self.Lobject = Lobject[:]
        self.numObj = len(Lobject)
        self.weight = weight
        self.tab = [[ Case() for j in range(self.weight+1)] for i in range(self.numObj+1)]

    def solve(self):# this algorithme is ussing a table of Case[number of object + 1][weight of the bag +1]
        for i in xrange(self.numObj+1):
            for j in xrange(self.weight+1):
                if j!=0 and i!=0:   #the first line stand for 0 object in the bag and the first colonne stand for a current weight of 0
                    if j-self.Lobject[i-1].weight >=0: # if the weight of the current object is lower or equall to the current weight
                        w = self.Lobject[i-1].weight# w is the weight of the current object
                        if self.tab[i-1][j].value > self.Lobject[i-1].value + self.tab[i-1][j-w].value: # if the value of the previous object at the current weight, is greater than the value of the current object plus the value of the previous object at the current weight minus the weight of the current object
                            self.tab[i][j].copy(self.tab[i-1][j])# then you just take the case of the previous object at the current weight
                        else:
                            self.tab[i][j].copy(self.tab[i-1][j-w])#otherwise you take the case of the previous object at the current weight minus w 
                            self.tab[i][j].addO(self.Lobject[i-1])# and you add the current object
                    else:# if if the weight of the current object his higher than the current weight then just copy the case of the previous object at the same weight
                        self.tab[i][j].copy(self.tab[i-1][j])
        print('objet')
        for i in self.Lobject:
            print i.name
        print('weight of the bag')
        print(self.weight)
        self.tab[self.numObj][self.weight].show()  


