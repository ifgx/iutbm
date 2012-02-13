#!/usr/bin/env python

import pygame
import sys
import math

import ui.theme as theme
import ui.rotatingMenu as rM
from algorithmes import voyage
from algorithmes import plus_court
from algorithmes import couplage
from algorithmes import sac_a_dos


class iutbm:
    '''
        main class
    '''
    def __init__(self, height, width):

        pygame.init()
        self.width = height
        self.height = width
        self.fpsLimit = 90

        self.display = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        # table of all algos
        self.drawalgo = ['QUIT', voyage.Voyage(self.display),
        plus_court.Graphe(self.display), couplage.Couplage(self.display),
        sac_a_dos.Sac_A_Dos(self.display)]

        # caption
        pygame.display.set_caption('IUTBM')

        #theme
        bg = pygame.image.load(theme.main_background)
        self.bg = pygame.transform.scale(bg, (self.width, self.height))#, None)

        # initialisation of the menu
        self.menu = rM.RotatingMenu(x=320, y=240, radius=220, arc=math.pi,
                defaultAngle = math.pi / 2.0)
        items = ['Exit', 'Saleman traveller', 'Shortest path',
                'Coupling', 'Backpack']
        [self.menu.addItem(rM.MenuItem(i)) for i in items]
        self.menu.selectItem(0)

    def main(self):
        inMenu = True
        inAlgo = False
        inHelp = False
        while True:
            button = None
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
                                algo.__init__(self.display)  # reset the algo
                                inMenu = False
                                inAlgo = True

                    elif inAlgo:
                        if event.key == pygame.K_h:
                            #h is the help key
                            inHelp = True
                            inAlgo = False

                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        # The escape and q key are bind to action INSIDE and OUTSIDE the menu
                        if inMenu:
                            sys.exit(0)
                        elif inAlgo:  # if we are inside an algo
                            inMenu = True
                            inAlgo = False
                        elif inHelp: # if we are inside a helpscreen
                            inAlgo = True
                            inHelp = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    button = event.button
                    if inMenu and button == 1:
                        item = self.menu.getCollisionItem(pos)
                        if item != -1:
                            self.menu.selectItem(item)
                            algo = self.drawalgo[item]
                            inMenu = False
                            inAlgo = True

            # update
            if inMenu:
                self.menu.update()
            elif inAlgo and pos != (0, 0)\
                    and button != None:
                algo._update(pos, button)

            # drawing's handling
            if inMenu:  # if we are inside the main menu
                self.display.blit(self.bg, (0, 0))  # main menu's background
                self.menu.draw(self.display)
            elif inAlgo:  # else if we are inside an algorithm
                self.display.fill((1, 0, 0))  #temp fix : please use a backgrounf for your algo !
                algo._draw()
            elif inHelp: # else if we are in a help screen
                self.display.fill((1, 0, 0))
                algo._explain()
            pygame.display.flip()  # draw on display
            self.clock.tick(self.fpsLimit)  # limit the fps


if __name__ == '__main__':
    a = iutbm(800, 600)
    a.main()
