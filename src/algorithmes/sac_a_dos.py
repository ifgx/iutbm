#!/bin/env python
# -*- coding: utf-8 -*-
import random

class Sac_A_Dos(object):
    '''
        The class Sac_A_Dos manages all the GUI
    '''
    def __init__(self, display):
        print "sac_a_dos :: init complete"
           
    def _draw(self):
        print "_draw called"
        
    def _update(self,pos, btn):
        print "_update called"
        
    def _explain(self):
        print "_explain called"
        
class Container(object):
    '''
        The class Container makes a GUI Imagery container
    '''
    
    def __init__(self,(xorg,yorg),(width,height),rows,cols,empty=False):
        self.position = (xorg, yorg)
        self.size = (width, height)
        self.rows = rows
        self.cols = cols
        self.objList = []
        if not empty: initObjList()
        
    def initObjList(self):
        for i in range(self.cols * self.rows):
            self.objList = OBJECT_LIST[i]
        
    def getClickedItemIndex(self,(mousex,mousey)):
        #Checking if mouse is accurate :
        x,y = self.position
        width, height = self.size
        
        if mousex < 0 or mousex > width or mousey < 0 or mousey > height :
            raise OutOfBoundException
        
        #Throwing back "array coordinates"
        col = (mousex - width / self.cols) % self.cols
        row = (mousey - height / self.rows) % self.rows
        return (col,row)
        
    def getItem(self,index):
        return self.objList[index]
        
    def setItem(self,index,name,pic,weight,value):
        self.objList[index] = Object(name, weight, value, pic)
        
    def setItemObject(self,obj,index):
        self.objList[index] = obj
        
    def clearItem(self,index):
        self.objList[index] = None
        
    def swapTo(self,container,index):
        tmp = container.getItem(index)
        container.setItemObject(self.getItem(index), index)
        self.setItemObject(tmp, index)
        
    def _draw(self):
        return "FIXME"


class Object(object):
    '''
        The class Object allow you to create object with a name, a value, and a weight
    '''

    def __init__(self, name, weight, value, pictpath):
        self.name = name
        self.weight = weight
        self.value = value
        self.rapport = self.value / self.weight
        self.pictpath = pictpath


class Case(object):
    '''
        The class Case allow you to create case which are used to solve the Bag problem
    '''
    def __init__(self):
        self.value = 0
        self.weight = 0
        self.content = []

    def copy(self, case):
        '''
            Copy case in the current object
        '''
        self.value = case.value
        self.weight = case.weight
        self.content = case.content[:]
    
    def addO(self,obj):
        '''
            add an object to the case
        '''
        self.value += obj.value
        self.weight += obj.weight
        self.content.append(obj)
    
    def show(self):
        print('value: %s' % self.value)
        print('weight: %s' % self.weight)
        print('Object: ' + ''.join([str(i.name) for i in self.content]))


class Bag(object):
    '''
        The class bag allow you to create bags
        who are defined by a list of object and a weight
    '''
    def __init__(self, Lobject, weight):
        self.Lobject = Lobject[:]
        self.numObj = len(Lobject)
        self.weight = weight
        self.tab = [[ Case() for j in range(self.weight + 1)] for i in range(self.numObj + 1)]

    def solve(self):
        '''
            This algorithm is using a table of Case[number of object + 1][weight of the bag +1]
        '''
        for i in xrange(self.numObj + 1):
            for j in xrange(self.weight + 1):
                if j != 0 and i != 0:
                    #the first line stand for 0 object in the bag and the first column
                    #stand for a current weight of 0
                    if j >= self.Lobject[i-1].weight:
                        w = self.Lobject[i-1].weight  # w is the weight of the current object
                        if self.tab[i-1][j].value > self.Lobject[i-1].value + self.tab[i-1][j-w].value:
                            #if the value of the previous object at the current weight,
                            #is greater than the value of the current object plus the value of the previous
                            #one at the current weight minus the weight of the current object
                            self.tab[i][j].copy(self.tab[i-1][j])
                            # then you just take the case of the previous object at the current weight
                        else:
                            self.tab[i][j].copy(self.tab[i-1][j-w])
                            #otherwise you take the case of the previous object at the current weight minus w 
                            self.tab[i][j].addO(self.Lobject[i-1])
                            #and add the current object
                    else:
                        # if the weight of the current object his higher than the current weight
                        #then just copy the case of the previous object at the same weight
                        self.tab[i][j].copy(self.tab[i-1][j])
                        
        print('object: ' + ''.join([i.name for i in self.Lobject]))
        print('weight of the bag: %s' % self.weight)
        self.tab[self.numObj][self.weight].show()  

L = []
for i in xrange(5):
    weight = random.randint(1,10)
    value = random.randint(1,10)
    L.append(Object(str(i),weight,value))    
    
bag = Bag(L,15)
