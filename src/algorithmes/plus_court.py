#!/bin/env python
# -*- coding: utf-8 -*-
import random
import pygame
import algo

from math import pi,cos,sin
from pygame.locals import *

class Graphe(algo.Algo):
    """
        A class that represent a connex graph
    """
    def __init__(self,window):
        algo.Algo.__init__(self, window)
        self.numSommet=8
        Min = 3
        Max = 10
        self.Matrix = [[float('inf') for i in xrange(self.numSommet)] for i in xrange(self.numSommet)]
        self.window = window
        """if Min > Max:
            print('Minimum in superior to maximum !')
            exit(1)
        """
        for i in xrange(self.numSommet - 1):
            weight = random.randint(Min, Max)
            self.Matrix[i][i+1] = weight
        for i in xrange(self.numSommet):
            for j in xrange(i):
                if i != j:
                    if self.Matrix[j][i] == float('inf'):
                        chance= random.random() * 100
                        if chance < 40:
                            weight = random.randint(Min, Max)
                            self.Matrix[j][i] = weight                
                    self.Matrix[i][j] = self.Matrix[j][i]
        self.center_x = window.get_width()/2
        self.center_y = window.get_height()/2
        if window.get_width() > window.get_height():
            self.rayon = window.get_height()/3
        else:
            self.rayon = window.get_width()/3
        self.LSommet = []
        for i in range(self.numSommet):
            x = self.center_x + cos(2*pi/self.numSommet*i)*self.rayon
            y = self.center_y + sin(2*pi/self.numSommet*i)*self.rayon
            self.LSommet.append(Sommet(i,i,x,y,'algorithmes/ville.jpg'))
        self.start=random.choice(self.LSommet).indice
        self.LSommet[self.start].score = 0
        self.end = (random.randint(1, self.numSommet-1) + self.start) % self.numSommet


    def _draw(self):
        for i in range(self.numSommet):
            for j in range(i):
                if (self.Matrix[i][j]!=float('inf')):
                    self.drawLien(i,j)
        for i in self.LSommet :
            i.drawItem(self.window)

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
            print(chemin.indice)
            chemin = chemin.previous

    def drawLien(self,i,j):
        start 	= self.LSommet[i].rect.center
        end = self.LSommet[j].rect.center        
        pygame.draw.line(self.window,(255,255,255),start,end,1)



    def _update(self,sommet1):
        for i in xrange(self.numSommet):
            if self.LSommet[i].score > sommet1.score + self.Matrix[sommet1.indice][i]:
                self.LSommet[i].score = sommet1.score + self.Matrix[sommet1.indice][i]
                self.LSommet[i].previous = sommet1

    def show(self):
        print('start: %s' % self.start)
        print('end: %s' % self.end)
        print(''.join([str(i) for i in self.Matrix]))
        

class Sommet(object):
    '''
        Define sommet with an indice, a score intialeted at 0, a boolean visited et a variable telling you the last the previous Sommet
    '''
    def __init__(self,indice,name,x,y,image):
        self.indice = indice
        self.score = float('inf')
        self.visited = False
        self.previous = None
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def drawItem(self,window):
        window.blit(self.image,self.rect)


def visiterS(x):
    if x.visited == False:
        return x.score
    else:
        return float('inf')


"""pygame.init()
screen = pygame.display.set_mode((300,400))
g=Graphe(7,1,2,screen)
screen.fill((255,255,255))

g.draw()
pygame.display.flip()
#BOUCLE INFINIE 
continuer = 1
while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 0"""
