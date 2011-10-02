from math import sin, cos, pi
import sys

import pygame


def sinInterpolation(start, end, steps=30):
    '''
        Calcul du placement
    '''
    values = []
    delta = end - start
    coef = pi / float(steps) / 2

    values = [start + delta * sin(i * coef) for i in xrange(1, steps)]
    values.insert(0, start)
    return values


class RotatingMenu:
    '''
        Represente le menu
    '''
    def __init__(self, x, y, radius, arc=pi*2, defaultAngle=0, wrap=True):
        '''
            x : centre du menu en x
            y : centre du menu en y
            radius : rayon du menu
            arc : arc du menu
            default Angle : angle de l'element selectionne
            wrap : si le menu wrap
        '''
        self.x = x
        self.y = y
        self.radius = radius
        self.arc = arc
        self.defaultAngle = defaultAngle
        self.wrap = wrap
        self.nbitems = 0

        self.rotation = 0
        self.rotationTarget = 0
        self.rotationSteps = [] #Used for interpolation

        self.items = []
        self.selectedItem = None
        self.selectedItemNumber = 0

    def addItem(self, item):
        '''
            ajoute un item au menu
        '''
        self.items.append(item)
        if len(self.items) == 1:
            self.selectedItem = item
        self.nbitems = float(len(self.items) - 1)

    def selectItem(self, itemNumber):
        '''
            Gestion du wrapping
        '''
        if self.wrap == True:
            if itemNumber > self.nbitems:
                itemNumber = 0
            elif itemNumber < 0:
                itemNumber = int(self.nbitems)
        else:
            itemNumber = min(itemNumber, self.nbitems)
            itemNumber = max(itemNumber, 0)

        self.selectedItem.deselect()
        self.selectedItem = self.items[itemNumber]
        self.selectedItem.select()

        self.selectedItemNumber = itemNumber

        self.rotationTarget = -self.arc * itemNumber / self.nbitems

        self.rotationSteps = sinInterpolation(self.rotation,
                                              self.rotationTarget, 45)

    def update(self):
        '''
            Mise a jour de coordonnees
        '''
        if self.rotationSteps:
            self.rotation = self.rotationSteps.pop(0)
            for j, i in enumerate(self.items):
                rot = self.defaultAngle + self.rotation + self.arc * j / self.nbitems
                i.x = self.x + cos(rot) * self.radius
                i.y = self.y + sin(rot) * self.radius


    def draw(self, display):
        '''
            Dessine le menu
        '''
        for item in self.items:
            display.blit(item.image, (item.x-item.xOffset, item.y-item.yOffset))

class MenuItem:
    '''
        Represente un item du menu
    '''
    def __init__(self, text='bleh'):
        self.text = text

        self.defaultColor = (255,255,255)
        self.selectedColor = (255,0,0)
        self.color = self.defaultColor

        self.x = 0
        self.y = 0 #The menu will edit these

        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, self.color)
        size = self.font.size(self.text)
        self.xOffset = size[0] / 2
        self.yOffset = size[1] / 2

    def select(self):
        '''
            Couleur du texte selectionne
        '''
        self.color = self.selectedColor
        self.redrawText()

    def deselect(self):
        '''
            Couleur du texte deselectionne
        '''
        self.color = self.defaultColor
        self.redrawText()

    def redrawText(self):
        '''
            Redessine le texte
        '''
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, self.color)
        size = self.font.size(self.text)
        self.xOffset = size[0] / 2
        self.yOffset = size[1] / 2

