'''
A nice and smooth rotating menu,
stolen from http://www.pygame.org/project-Rotating+Menu-975-.html.
original author : Francesco Mastellone (effeemme)
'''
from math import sin, cos, pi
import sys

import pygame

def sinInterpolation(start, end, steps=30):
    '''
        Placement stuffs
    '''
    values = []
    delta = end - start
    coef = pi / float(steps) / 2

    values = [start + delta * sin(i * coef) for i in xrange(1, steps)]
    values.insert(0, start)
    return values


class RotatingMenu:
    '''
        Implement the rotating menu
    '''
    def __init__(self, x, y, radius, arc=pi*2, defaultAngle=0, wrap=True):
        '''
            x : x's position of the menu's center
            y : y's position of the menu's center
            radius : radius of the menu
            arc : arc of the menu
            default Angle : angle of selected item
            wrap : does the menu wrap ?
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
            add an item to the menu
        '''
        self.items.append(item)
        if len(self.items) == 1:
            self.selectedItem = item
        self.nbitems = float(len(self.items) - 1)

    def selectItem(self, itemNumber):
        '''
            Wrapping stuffs
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
            Coord's update
        '''
        if self.rotationSteps:
            self.rotation = self.rotationSteps.pop(0)
            for j, i in enumerate(self.items):
                rot = self.defaultAngle + self.rotation + self.arc * j / self.nbitems
                i.x = self.x + cos(rot) * self.radius
                i.y = self.y + sin(rot) * self.radius

    def getCollisionItem(self,(x,y)):
        for j, i in enumerate(self.items):
            if i.get_rect().collidepoint(x,y):
                return j

        return -1

    def draw(self, display):
        '''
            Draw the menu
        '''
        for item in self.items:
            display.blit(item.shadow, ((item.x - item.xOffset) + 1, (item.y - item.yOffset) + 1))
            display.blit(item.image, (item.x-item.xOffset, item.y-item.yOffset))

class MenuItem:
    '''
        Implement an item's menu
    '''
    def __init__(self, text='fill_me_please'):
        self.text = text

        self.defaultColor = (255,255,255)
        self.selectedColor = (255,0,0)
        self.color = self.defaultColor

        self.x = 0
        self.y = 0 #The menu will edit these

        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, self.color)
        self.shadow = self.font.render(self.text, True, (0, 0, 0))
        self.size = self.font.size(self.text)
        self.xOffset = self.size[0] / 2
        self.yOffset = self.size[1] / 2

    def select(self):
        '''
            Selected text's color
        '''
        self.color = self.selectedColor
        self.redrawText()

    def deselect(self):
        '''
            Not selected text's color
        '''
        self.color = self.defaultColor
        self.redrawText()

    def redrawText(self):
        '''
            Redraw the text
        '''
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, self.color)
        self.shadow = self.font.render(self.text, True, (0, 0, 0))
        self.size = self.font.size(self.text)
        self.xOffset = self.size[0] / 2
        self.yOffset = self.size[1] / 2

    def get_rect(self):
        return pygame.Rect(self.x - self.size[0] / 2,self.y - self.size[1] / 2,self.size[0],self.size[1])
