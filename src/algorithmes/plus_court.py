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
        self.numSommet=7
        Min = 3
        Max = 20
        
        self.window = window
        self.center_x = window.get_width()/2
        self.center_y = window.get_height()/2
        if window.get_width() > window.get_height():
            self.rayon = window.get_height()/3
        else:
            self.rayon = window.get_width()/3
        self.LSommet = []
        for i in range(self.numSommet):
            x = self.center_x + cos(2*pi/(self.numSommet-2)*i)*self.rayon
            y = self.center_y + sin(2*pi/(self.numSommet-2)*i)*self.rayon
            self.LSommet.append(Sommet(i,i,x,y,'algorithmes/ville.jpg'))
        self.start=self.LSommet[0]
        self.start.rect.center=(self.center_x/3,self.center_y/3)

        self.end = self.LSommet[self.numSommet-1]
        self.end.rect.center=(self.center_x*5/3,self.center_y*5/3)
        self.LSommet[self.start.indice].score = 0

        # creation de la matrice d'adjacence
        self.Matrix = [[float('inf') for i in xrange(self.numSommet)] for i in xrange(self.numSommet)]
        for i in xrange(self.numSommet):
            if i < self.numSommet - 1:
                weight = random.randint(Min, Max)
                self.Matrix[i][i+1] = weight   
            for j in xrange(i):
                if i != j:
                    if self.Matrix[j][i] == float('inf'):
                        chance= random.random() * 100
                        if chance <30:
                            weight = random.randint(Min, Max)
                            self.Matrix[j][i] = weight                
                    self.Matrix[i][j] = self.Matrix[j][i]

        # the two next line are to make sure that there is not  a direct connenxion between the start and the end
        self.Matrix[self.start.indice][self.end.indice]= float('inf')
        self.Matrix[self.end.indice][self.start.indice]= float('inf')
        
        self.final = False
        self.weight = 0
        self.current = self.start
        self.next = []
        self.selected = []
        self.nextSommet(self.start)

    def _draw(self):
        if self.final == False:
            font = pygame.font.Font(None, 30)
            text = font.render("Valeur actuel :"+str(self.weight), True, (0,255, 0))
            textRect = text.get_rect()
            textRect.top = 30
            textRect.left = 30
            self.window.blit(text,textRect)        
            for i in range(self.numSommet):
                for j in range(i):
                    if (self.Matrix[i][j]!=float('inf')):
                        self.drawLien(i,j)
            for i in self.LSommet :
                i.drawItem(self.window)
            for i in self.selected:
                i.drawSelected(self.window)
            pygame.draw.rect(self.window,(255,0,0),self.start.rect, 1)
            pygame.draw.rect(self.window,(0,255,0),self.end.rect, 1)
        else:
            font = pygame.font.Font(None,20)
            text = font.render("Vous avez trouvé une valeur de "+str(self.weight)+"\nLa valeur optimale est de "+str(self.end.score),True , (0,255,0))
            textRect = text.get_rect()
            textRect.center =(self.center_x,self.center_y)
            self.window.blit(text,textRect)

    def _solve(self):
        NotChecked = self.LSommet[:]
        while NotChecked:
            sommet1 = min(NotChecked, key = visiterS)
            sommet1.visited  = True
            NotChecked.remove(sommet1)
            self.misejour(sommet1)
        self.final = True

    def misejour(self,sommet1):
        for i in xrange(self.numSommet):
            if self.Matrix[sommet1.indice][i]+sommet1.score < self.LSommet[i].score:
                self.LSommet[i].score = self.Matrix[sommet1.indice][i]+sommet1.score


    def drawLien(self,i,j):
        start     = self.LSommet[i].rect.center
        end = self.LSommet[j].rect.center   
        middle = ((end[0]+start[0])/2 ,(end[1]+start[1])/2)
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.Matrix[i][j]), True, (0,255, 0))
        textRect = text.get_rect()
        textRect.center = middle    
        pygame.draw.line(self.window,(255,255,255),start,end,3)
        self.window.blit(text,textRect)

    def nextSommet(self, sommet):
        self.next = []
        self.current = sommet
        for i in self.LSommet:
            if self.Matrix[sommet.indice][i.indice] != float('inf'):
                self.next.append(i)

    def show(self):
        print('start: %s' % self.start.indice)
        print('end: %s' % self.end)
        print(''.join([str(i) for i in self.Matrix]))

    def _update(self,(x,y)):
        for i in self.LSommet:
            if i.rect.collidepoint(x,y) :
                if i == self.start:
                    self.weight = 0
                    self.selected = []
                    self.nextSommet(i)
                if i in set(self.next):
                    self.weight += self.Matrix[self.current.indice][i.indice]
                    self.selected.append(i)
                    self.nextSommet(i)
                    if i == self.end:
                        self._solve()

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

    def drawSelected(self,window):
        pygame.draw.rect(window,(255,0,255),self.rect, 1)


def visiterS(x):
    if x.visited == False:
        return x.score
    else:
        return float('inf')

