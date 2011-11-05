#!/bin/env python

import pygame
import sys
import math

from ui import rotatingMenu as rM
from algorithmes import voyage
from algorithmes import plus_court


class iutbm:
    '''
        main class
    '''
    def __init__(self, height, width):

        pygame.init()
        self.width = height
        self.height = width
        self.fpsLimit = 90

        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # table of all algos
        self.drawalgo = ['QUIT', voyage.Voyage(self.display),
        plus_court.Graphe(self.display), 'FIXME', 'FIXME', 'FIXME']

        # caption
        pygame.display.set_caption('IUTBM')

        # initialisation of the menu
        self.menu = rM.RotatingMenu(x=320, y=240, radius=220, arc=math.pi,
                defaultAngle = math.pi / 2.0)
        items = ['quit', 'saleman traveller', 'plus court chemin',
                'couplage', 'sac a dos', 'confiserie']
        [self.menu.addItem(rM.MenuItem(i)) for i in items]
        self.menu.selectItem(0)

    def main(self):
        inMenu = True
        inAlgo = False
        while True:
            pos = (0, 0)  # reset mouse position
            # events handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if inMenu:  # if we are in the menu
                        if event.key == pygame.K_LEFT:
                            self.menu.selectItem(self.menu.selectedItemNumber + 1)
                        elif event.key == pygame.K_RIGHT:
                            self.menu.selectItem(self.menu.selectedItemNumber - 1)
                        elif event.key == pygame.K_UP or event.key == pygame.K_RETURN:  # selection of the current item
                            if self.menu.selectedItemNumber == 0:  # "the quit" item
                                sys.exit(0)
                            else:
                                algo = self.drawalgo[self.menu.selectedItemNumber]
                                inMenu = False
                                inAlgo = True
                    if event.key == pygame.K_ESCAPE:
                        # The escape key is bind to action INSIDE and OUTSIDE the menu
                        if inMenu:
                            sys.exit(0)
                        elif inAlgo:  # if we are inside an algo
                            inMenu = True
                            inAlgo = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        pos = event.pos

            # update
            if inMenu:
                self.menu.update()
            elif inAlgo:
                if pos != (0, 0):
                    algo._update(pos)

            # drawing's handling
            self.display.fill((0, 0, 0))  # black background
            if inMenu:  # if we are inside a menu
                self.menu.draw(self.display)
            elif inAlgo:  # if we are inside an algorithm
                algo._draw()
            pygame.display.flip()  # draw on display
            self.clock.tick(self.fpsLimit)  # limit the fps


if __name__ == '__main__':
    a = iutbm(800, 600)
    a.main()
