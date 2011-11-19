'''
    Shortest path problem
'''

import random
import pygame
import algo

import math


class Graphe(algo.Algo):
    '''
        A class that represent a connex graph
    '''
    def __init__(self,window):
        algo.Algo.__init__(self, window)
        self.numSommet = 9 # the number of Sommet in the game
        self.state_game = self.weight = 0 # the state 0 correspond to the usall state of the game
        # the state 1 correspond to the end of the game
        self.next_sommet = [] # next_sommet is a list of the sommet that are avaible from the current sommet
        self.selected = [] # list of the sommet that are currently selected
        
        self.start = None
        self.current = None 
        self.end = None
        self.LSommet = []

        self.init_LSommet()

        # creation of an adjacency matrix 
        self.Matrix = [[float('inf') for i in xrange(self.numSommet)] for i in xrange(self.numSommet)]

        minimum_weight = 3 
        maximum_weight = 20 
        self.init_connex(minimum_weight,maximum_weight)
        self.init_add_link(minimum_weight,maximum_weight)

        self.nextSommet(self.start)


    def init_LSommet(self):
        # creation of the list of sommet and the coordonate by using a circle
        rayon = 35
        tmp = 2 * math.pi / (self.numSommet - 2)
        self.LSommet.append(Sommet(0, 10, 10, 'algorithmes/ville.jpg'))
        for i in xrange(self.numSommet-2):
            x = 50 + math.cos(tmp * i) * rayon
            y = 50 + math.sin(tmp * i) * rayon
            self.LSommet.append(Sommet(i, x, y, 'algorithmes/ville.jpg'))
        self.LSommet.append(Sommet(self.numSommet - 1, 90, 90, 'algorithmes/ville.jpg'))
        self.start = self.LSommet[0]
        self.current = self.start
        self.LSommet[self.start.indice].score = 0

        self.end = self.LSommet[self.numSommet - 1]


    def init_connex(self,minimum_weight, maximum_weight):
        # creation of a connex graphe
        a = [i for i in xrange(self.numSommet - 1)]
        current = 0 
        for i in xrange(self.numSommet - 1):
            weight = random.randint(minimum_weight, maximum_weight)
            if i < self.numSommet - 2:
                a.remove(current)
                next_point = random.sample(a, 1)
                self.Matrix[current][next_point[0]] = weight
                self.Matrix[next_point[0]][current] = weight
                current = next_point[0]
            else:
                self.Matrix[current][self.numSommet - 1] = weight
                self.Matrix[self.numSommet - 1][current] = weight


    def init_add_link(self,minimum_weight,maximum_weight):
        # adittion of some link 
        for i in xrange(self.numSommet):
            for j in xrange(i):
                if i != j:
                    if self.Matrix[j][i] == float('inf'):
                        chance = random.random() * 100
                        if chance <40:  
                            # there is 40 % chance that we will create a new link between the two sommet
                            weight = random.randint(minimum_weight, maximum_weight)
                            self.Matrix[j][i] = weight
                    self.Matrix[i][j] = self.Matrix[j][i]

        # make sure that the is no direct connection between
        # the start point, and the end point.
        self.Matrix[self.start.indice][self.end.indice]= float('inf')
        self.Matrix[self.end.indice][self.start.indice]= float('inf')


    def _draw(self):
        # calculate of the coordinate relative to the screen
        for i in self.LSommet:
            i.rect.center = self._get_corres_pixel(i.x,i.y)
        text = self.font.render("User: " + str(self.weight) + "    Path: " + ', '.join([str(i.indice) for i in self.selected]), True, (0,255, 0) )
        textRect = text.get_rect()
        textRect.top = textRect.left = 30
        self.display.blit(text,textRect)
        for i in xrange(self.numSommet): 
            [self.drawLien(i, j) for j in xrange(i) if self.Matrix[i][j] != float('inf')]# if the link between two point is define in the matrix then we draw the link 

        [self.display.blit(i.image, i.rect) for i in self.LSommet]# then we draw the picture of the town
        [pygame.draw.rect(self.display, (255, 0, 255), i.rect,2) for i in self.selected]# then we draw the weight of the link
        pygame.draw.rect(self.display,(255,0,0),self.start.rect,2)
        pygame.draw.rect(self.display,(0,255,0),self.end.rect,2)

        if self.state_game == 1: 
            if (self.weight > self.end.score):
                text = self.font.render("You did not found the optimal path",True , (0,255,0))
            else:
                text = self.font.render("Congratulation : you found the optimal path wiht the lenght " + str(self.end.score).replace('[',' '),True , (0,255,0))
            textRect = text.get_rect()
            textRect.center =(self.display.get_width()/2, 10)
            self.display.blit(text,textRect)

    def _solve(self):
        NotChecked = self.LSommet[:]
        while NotChecked:
            sommet1 = min(NotChecked, key = lambda x : x.visited == False and x.score or float('inf'))
            sommet1.visited  = True
            NotChecked.remove(sommet1)
            self.misejour(sommet1)
        self.state_game = 1

    def _update(self, (x, y),button): 
        if button == 1:
            for i in self.LSommet: # for all the sommet in the graphe
                if i.rect.collidepoint(x, y) : # if the current position of the mouse is over the rect of the sommet
                    if i == self.start: # if this sommet is the start then we go back to the start
                        self.weight = self.state_game = 0
                        self.selected = []
                        self.nextSommet(i)
                    if i in set(self.next_sommet)  and self.end not in self.selected: # if the sommet is one of sommet in list of the next sommet avaible
                        self.weight += self.Matrix[self.current.indice][i.indice] # then you add at the current weight the weight of the selected sommet
                        self.selected.append(i) 
                        self.nextSommet(i)
                        self.state_game = 0 # we are in the state 0
                        if i == self.end: # if the sommet is the end we solve the graphe
                            self._solve()
        if button == 3:
            self.state_game = 0
            if len(self.selected)<=1:
                self.selected = []
                self.weight = 0
                self.nextSommet(self.start)
            else:
                tmp=self.selected.pop()
                self.nextSommet(self.selected[-1])
                self.weight -= self.Matrix[tmp.indice][self.selected[-1].indice]


    def middle(self, sommet2, sommet1): # return a tuple what is the middle of the segement  between the two sommet
        x = sommet2.centery- sommet1.centery
        y = sommet1.centerx - sommet2.centerx
        k = 15 / (math.sqrt(x*x+y*y))
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
        position = self.middle(start,end)
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.Matrix[i][j]), True, (255,255, 255),(0,0,0))
        textRect = text.get_rect()
        textRect.center = position
        pygame.draw.line(self.display,(0,0,255),start.center,end.center,3)
        self.display.blit(text,textRect)

    def nextSommet(self, sommet):
        self.next_sommet = []
        self.current = sommet
        for i in self.LSommet:
            if self.Matrix[sommet.indice][i.indice] != float('inf'):
                self.next_sommet.append(i)

class Sommet(object):
    '''
        Implement a "Sommet":
    '''
    def __init__(self, indice, x, y, image):
        self.indice = indice
        self.score = float('inf') # the score of the sommet ,at the beginning the value is +infini 
        self.visited = False # if the sommet has been visited
        self.previous = None  # the previous Sommet
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.x,self.y = x,y # position if the width and the height of the screen are both equal to 100

