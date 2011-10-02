#!/bin/env python

import pygame
import sys
import math

#import ui
from ui import rotatingMenu as rM

class iutbm:
    '''
        Classe principale
    '''
    def __init__(self, height, width):
        pygame.init()
        self.width = height
        self.height = width
        self.fpsLimit = 90

        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        #initialisation du menu
        self.menu = rM.RotatingMenu(x=320, y=240, radius=220, arc=math.pi,
                defaultAngle=math.pi/2.0)
        items = ['quitter', 'voyageur de commerce', 'plus court chemin',
                'couplage', 'sac a dos', 'confiserie']
        [self.menu.addItem(rM.MenuItem(i)) for i in items]
        self.menu.selectItem(0)

    def main(self):
        while True:
            #gestion des evenements
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.menu.selectItem(self.menu.selectedItemNumber + 1)
                    elif event.key == pygame.K_RIGHT:
                        self.menu.selectItem(self.menu.selectedItemNumber - 1)
                    elif event.key == pygame.K_UP:
                        if self.menu.selectedItemNumber == 0:
                            sys.exit(0)
                        print self.menu.selectedItemNumber

            # mis a jour du menu
            self.menu.update()

            #dessin
            self.display.fill((0, 0, 0)) # fond noir
            self.menu.draw(self.display)
            pygame.display.flip()
            self.clock.tick(self.fpsLimit)


if __name__ == '__main__':
    a = iutbm(800, 600)
    a.main()
