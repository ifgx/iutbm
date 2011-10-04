#!/bin/env python
# -*- coding: utf-8 -*-
import random


class Graphe(object):
    """
        A class that allow you to create connexe graphe
    """
    def __init__(self,numSommet,Min,Max):
        self.Matrix = [[ float('inf') for i in xrange(numSommet)] for i in xrange(numSommet)]
        self.numSommet = numSommet
        if(Min > Max):
            exit()
        for i in xrange(numSommet - 1):
            weight = random.randint(Min, Max)
            self.Matrix[i][i+1] = weight
        for i in xrange(numSommet):
            for j in xrange(i):
                if i == j:
                    pass
                else:
                    if self.Matrix[j][i] == float('inf'):
                        chance= random.random() * 100
                        if chance < 40:
                            weight = random.randint(Min, Max)
                            self.Matrix[j][i] = weight                
                    self.Matrix[i][j] = self.Matrix[j][i]
        self.LSommet = [Sommet(i) for i in xrange(numSommet)]
        self.start=random.choice(self.LSommet).indice
        self.LSommet[self.start].score = 0
        self.end = (random.randint(1, numSommet-1) + self.start) % numSommet


    def solve(self):
        NotChecked = self.LSommet[:]
        while NotChecked:
            sommet1 = min(NotChecked, key = visiterS)
            sommet1.visited  = True
            NotChecked.remove(sommet1)
            self.update(sommet1)
        print('resultat : \n')
        print(self.LSommet[self.end].score)
        chemin = self.LSommet[self.end].previous
        while chemin != None:
            print chemin.indice
            chemin = chemin.previous


    def update(self,sommet1):
        for i in xrange(self.numSommet):
            if self.LSommet[i].score > sommet1.score + self.Matrix[sommet1.indice][i]:
                self.LSommet[i].score = sommet1.score + self.Matrix[sommet1.indice][i]
                self.LSommet[i].previous = sommet1

    def show(self):
        print('Sommet de début')
        print(self.start)
        print('Sommet de fin')
        print(self.end)
        print(''.join([i for i in self.Matrix]))
    	




'''
    class Sommet allow you to define sommet with an indice, a score intialeted at 0, a boolean visited et a variable telling you the last the previous Sommet
'''
class Sommet(object):
    def __init__(self,indice):
        self.indice = indice
        self.score = float('inf')
        self.visited = False
        self.previous = None

def visiterS(x):
    if x.visited == False:
        return x.score
    else:
        return float('inf')

g=Graphe(10,2,9)
g.solve()
