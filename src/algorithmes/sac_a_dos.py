#!/bin/env python
# -*- coding: utf-8 -*-
import random
import pygame
import algo

class Sac_A_Dos(algo.Algo):
    '''
        The class Sac_A_Dos manages the whole game
    '''

    def __init__(self, display):
        algo.Algo.__init__(self, display)
        picRoot = "ui/pix/couplage/"

        self.allIngredients = [
            Object("Chorizo",1,2,picRoot + "client-blanc.png"),
            Object("Herbs",2,3,picRoot + "client-bleu.png"),
            Object("Olive oil",4,5,picRoot + "client-orange.png"),
            Object("Garlic",6,7,picRoot + "client-vert.png"),
            Object("Onion",7,8,picRoot + "client-violet.png"),
            Object("Cheese",7,8,picRoot + "client-violet.png"),
            Object("Mushrooms",7,8,picRoot + "client-violet.png"),
            Object("Minced Meat",7,8,picRoot + "client-violet.png"),
            Object("Cream",7,8,picRoot + "client-violet.png"),
            Object("Salmon",7,8,picRoot + "client-violet.png"),
            Object("Peppers",7,8,picRoot + "client-violet.png"),
            Object("Seafood",7,8,picRoot + "client-violet.png")
        ]
        self.ingredients = random.sample(self.allIngredients, 5)

    def _update(self, (x, y),button):
        for i in self.ingredients:
            if button == 1 and i.collidewith(x,y):
                i.swapInBag()

    def _draw(self):
        #Legend 1
        titre = self.font.render("Help the pizzaiolo choosing the best ingredients for the pizza contest", True, (255, 255, 255) )
        titreRect = titre.get_rect()
        titreRect.top = 48
        titreRect.centerx = self.display.get_rect().width / 2
        self.display.blit(titre, titreRect)

        #Legend 2
        titre = self.font.render("Red number shows weight, green number shows the value.", True, (255, 255, 255) )
        titreRect = titre.get_rect()
        titreRect.top = 64
        titreRect.centerx = self.display.get_rect().width / 2
        self.display.blit(titre, titreRect)

        for c,i in enumerate(self.ingredients):
            if i.inBag:
                ingx = 600
            else:
                ingx = 200

            i.draw(self.display,self.font,ingx,c*64+128)

    def _explain(self):
        return None

class Object(object):
    '''
        The class Object allow you to create object with a name, a value, and a weight
    '''

    def __init__(self, name, weight, value, pict):
        self.name = name
        self.weight = weight
        self.value = value
        self.rapport = self.value / self.weight
        self.pict = pygame.image.load(pict)
        self.inBag = False
        self.posx = None
        self.posy = None

    def draw(self,display,font,x,y):
        #Affichage image
        self.posx = x
        self.posy = y
        display.blit(self.pict, (x,y))

        #Affichage sous-titre
        objn = font.render(self.name, True, (255, 255, 255) )
        objnRect = objn.get_rect()
        objnRect.top = y + self.pict.get_rect().bottom
        objnRect.centerx = x + self.pict.get_rect().right / 2
        display.blit(objn, objnRect)

        #Affichage poids
        objn = font.render(str(self.weight), True, (255, 0, 0) )
        objnRect = objn.get_rect()
        objnRect.top = y + self.pict.get_rect().bottom / 4
        objnRect.centerx = x + self.pict.get_rect().right + 5
        display.blit(objn, objnRect)

        #Affichage valeur
        objn = font.render(str(self.weight), True, (0, 255, 0) )
        objnRect = objn.get_rect()
        objnRect.top = y + (self.pict.get_rect().bottom / 4) * 3
        objnRect.centerx = x + self.pict.get_rect().right + 5
        display.blit(objn, objnRect)

    def swapInBag(self):
        self.inBag = not self.inBag

    def collidewith(self,x,y):
        imgrect = self.pict.get_rect()
        return self.posx < x < self.posx + imgrect.right \
            and self.posy < y < self.posy + imgrect.bottom

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

#L = []
#for i in xrange(5):
#    weight = random.randint(1,10)
#    value = random.randint(1,10)
#    L.append(Object(str(i),weight,value))    
    
#bag = Bag(L,15)
