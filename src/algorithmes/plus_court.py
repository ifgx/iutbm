import random
import pygame
import algo

from math import pi,cos,sin, sqrt
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
        self.center_x = self.display.get_width()/2
        self.center_y = self.display.get_height()/2
        if self.display.get_width() > self.display.get_height():
            self.rayon = self.display.get_height()/3
        else:
            self.rayon = self.display.get_width()/3
        self.LSommet = []
        # creation de la liste de point et de leur position
        for i in xrange(self.numSommet):
            x = self.center_x + cos(2*pi/(self.numSommet-2)*i)*self.rayon
            y = self.center_y + sin(2*pi/(self.numSommet-2)*i)*self.rayon
            self.LSommet.append(Sommet(i,i,x,y,'algorithmes/ville.jpg'))
        self.start=self.LSommet[0]
        self.start.rect.center=(self.center_x/3,self.center_y/3)
        self.LSommet[self.start.indice].score = 0

        self.end = self.LSommet[self.numSommet-1]
        self.end.rect.center=(self.center_x*5/3,self.center_y*5/3)

        # creation de la matrice d'adjacence
        self.Matrix = [[float('inf') for i in xrange(self.numSommet)] for i in xrange(self.numSommet)]

        # creation d'un graphe connexe aleatoire
        a = [i for i in xrange(self.numSommet - 1)]
        now = 0
        for i in xrange(self.numSommet-1):
            weight = random.randint(Min,Max)
            if i < self.numSommet - 2:
                a.remove(now)
                next = random.sample(a,1)
                self.Matrix[now][next[0]] = weight
                self.Matrix[next[0]][now] = weight
                now = next[0]
            else:
                self.Matrix[now][self.numSommet-1] = weight
                self.Matrix[self.numSommet - 1][now] = weight
        for i in xrange(self.numSommet):
            for j in xrange(i):
                if i != j:
                    if self.Matrix[j][i] == float('inf'):
                        chance= random.random() * 100
                        if chance <40:
                            weight = random.randint(Min, Max)
                            self.Matrix[j][i] = weight
                    self.Matrix[i][j] = self.Matrix[j][i]

        # the two next line are to make sure that there is not  a direct connenxion between the start and the end
        self.Matrix[self.start.indice][self.end.indice]= float('inf')
        self.Matrix[self.end.indice][self.start.indice]= float('inf')

        self.final = 0
        self.weight = 0
        self.current = self.start
        self.next = []
        self.selected = []
        self.nextSommet(self.start)

    def _draw(self):
        if self.final == 0 or self.final == 1:
            font = pygame.font.Font(None, 30)
            text = font.render("Valeur actuel :"+str(self.weight), True, (0,255, 0))
            textRect = text.get_rect()
            textRect.top = 30
            textRect.left = 30
            self.display.blit(text,textRect)
            for i in xrange(self.numSommet):
                for j in xrange(i):
                    if (self.Matrix[i][j]!=float('inf')):
                        self.drawLien(i,j)
            for i in self.LSommet :
                self.display.blit(i.image, i.rect)
            for i in self.selected:
                pygame.draw.rect(self.display, (255,0,255), i.rect)
            pygame.draw.rect(self.display,(255,0,0),self.start.rect, 1)
            pygame.draw.rect(self.display,(0,255,0),self.end.rect, 1)
        if self.final == 1:
            font = pygame.font.Font(None,20)
            if (self.weight > self.end.score):
                text = font.render("Vous avez trouve une valeur de "+str(self.weight)+"Il ne s'agit pas de la valeur optimale",True , (0,255,0))
            else:
                text = font.render("Felicitation vous avez trouve la valeur optimale "+str(self.end.score),True , (0,255,0))
            textRect = text.get_rect()
            textRect.center =(self.center_x,10)
            self.display.blit(text,textRect)
#        if self.final == 2:


    def _help(self):
        if self.final == 2:
            self.final = 0
        else:
            self.final = 2
    def _solve(self):
        NotChecked = self.LSommet[:]
        while NotChecked:
            sommet1 = min(NotChecked, key = visiterS)
            sommet1.visited  = True
            NotChecked.remove(sommet1)
            self.misejour(sommet1)
        self.final = 1

    def _update(self,(x,y)):
        for i in self.LSommet:
            if i.rect.collidepoint(x,y) :
                if i == self.start:
                    self.weight = 0
                    self.selected = []
                    self.nextSommet(i)
                    self.final = 0
                if i in set(self.next):
                    self.weight += self.Matrix[self.current.indice][i.indice]
                    self.selected.append(i)
                    self.nextSommet(i)
                    self.final = 0
                    if i == self.end:
                        self._solve()

    def coordonner(self,sommet2,sommet1):
        x = sommet2.centery- sommet1.centery
        y = sommet1.centerx - sommet2.centerx
        k = 15 / (sqrt(x*x+y*y))
        x = k*x + (sommet2.centerx + sommet1.centerx ) / 2
        y = k*y + (sommet2.centery + sommet1.centery ) / 2
        return (x,y)

    def misejour(self,sommet1):
        for i in xrange(self.numSommet):
            if self.Matrix[sommet1.indice][i]+sommet1.score < self.LSommet[i].score:
                self.LSommet[i].score = self.Matrix[sommet1.indice][i]+sommet1.score


    def drawLien(self,i,j):
        start     = self.LSommet[i].rect
        end = self.LSommet[j].rect
        position = self.coordonner(start,end)
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.Matrix[i][j]), True, (0,255, 0),(0,0,100))
        textRect = text.get_rect()
        textRect.center = position
        pygame.draw.line(self.display,(255,255,255),start.center,end.center,3)
        self.display.blit(text,textRect)

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

    def drawItem(self):
        self.display.blit(self.image,self.rect)

    def drawSelected(self):
        pygame.draw.rect(self.display,(255,0,255),self.rect, 1)


def visiterS(x):
    if x.visited == False:
        return x.score
    else:
        return float('inf')

