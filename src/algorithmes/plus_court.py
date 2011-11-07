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
        self.numSommet = 7
        minimum_weight = 3 
        maximum_weight = 20 
        self.state_game = self.weight = 0 # the state 0 correspond to the usall state of the game
        # the state 1 correspond to the end of the game
        # the state 2 correspond to the state of help
        self.next = [] # next sommet that are avaible from the current sommet
        self.selected = [] # the list of the sommet that are currently selected

        self.center_x = self.display.get_width() / 2
        self.center_y = self.display.get_height() / 2
        if self.display.get_width() > self.display.get_height():
            self.rayon = self.display.get_height() / 3
        else:
            self.rayon = self.display.get_width() / 3

        self.LSommet = []
        # creation of the list of sommet and the coordonate
        tmp = 2 * math.pi / (self.numSommet - 2)
        for i in xrange(self.numSommet):
            x = self.center_x + math.cos(tmp * i) * self.rayon
            y = self.center_y + math.sin(tmp * i) * self.rayon
            self.LSommet.append(Sommet(i, x, y, 'algorithmes/ville.jpg'))
        self.start = self.LSommet[0]
        self.current = self.start
        self.start.rect.center = (self.center_x / 3, self.center_y / 3)
        self.LSommet[self.start.indice].score = 0

        self.end = self.LSommet[self.numSommet - 1]
        self.end.rect.center=(self.center_x* 1.6,self.center_y * 1.6)

        # creation of an adjacency matrix 
        self.Matrix = [[float('inf') for i in xrange(self.numSommet)] for i in xrange(self.numSommet)]

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

        # adittion of some link 
        for i in xrange(self.numSommet):
            for j in xrange(i):
                if i != j:
                    if self.Matrix[j][i] == float('inf'):
                        chance = random.random() * 100
                        if chance <40:  # there is 40 % chance that we will create a new link between the two sommet
                            weight = random.randint(minimum_weight, maximum_weight)
                            self.Matrix[j][i] = weight
                    self.Matrix[i][j] = self.Matrix[j][i]

        # make sure that the is no direct connection between
        # the start point, and the end point.
        self.Matrix[self.start.indice][self.end.indice]= float('inf')
        self.Matrix[self.end.indice][self.start.indice]= float('inf')

        self.nextSommet(self.start)

    def _draw(self):
        if self.state_game == 0 or self.state_game == 1: # if we are in the state 0 or 1
            text = self.font.render("User: " + str(self.weight) + "Path: " + str([i.indice for i in self.selected]), True, (0,255, 0) )
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
                text = self.font.render("Congratulation : you found the optimal path wiht the lenght " + str(self.end.score),True , (0,255,0))
            textRect = text.get_rect()
            textRect.center =(self.center_x, 10)
            self.display.blit(text,textRect)

    def _help(self): #FIXME : wtf ?
        if self.state_game == 2:
            self.state_game = 0
        else:
            self.state_game = 2

    def _solve(self):
        NotChecked = self.LSommet[:]
        while NotChecked:
            sommet1 = min(NotChecked, key =visiterS )
            sommet1.visited  = True
            NotChecked.remove(sommet1)
            self.misejour(sommet1)
        self.state_game = 1

    def _update(self, (x, y)): 
        for i in self.LSommet: # for all the sommet in the graphe
            if i.rect.collidepoint(x, y) : # if the current position of the mouse is over the rect of the sommet
                if i == self.start: # if this sommet is the start then we go back to the start
                    self.weight = self.state_game = 0
                    self.selected = []
                    self.nextSommet(i)
                if i in set(self.next): # if the sommet is one of sommet in list of the next sommet avaible
                    self.weight += self.Matrix[self.current.indice][i.indice] # then you add at the current weight the weight of the selected sommet
                    self.selected.append(i) 
                    self.nextSommet(i)
                    self.state_game = 0 # we are in the state 0
                    if i == self.end: # if the sommet is the end we solve the graphe
                        self._solve()

    def middle(self, sommet2, sommet1): # return a tuple what is the middle of the segement between the two sommet
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
        Implement a "Sommet":
    '''
    def __init__(self, indice, x, y, image):
        self.indice = indice
        self.score = float('inf')
        self.visited = False
        self.previous = None  # the previous Sommet
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


def visiterS(x): #FIXME : wtf ? Inline this !
    if x.visited == False:
        return x.score
    else:
        return float('inf')

