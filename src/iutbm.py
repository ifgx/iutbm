#!/usr/bin/env python

import pygame
import sys
import math

import ui.theme as theme
import ui.rotatingMenu as rM
import ui.buttonMenu as bM
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
        self.menu = bM.Menu(
                  [("salesman", (0, 0), voyage.Voyage(self.display)),
                   ("shortest", (1, 0), plus_court.Graphe(self.display)),
                   ("coupling", (2, 0), couplage.Couplage(self.display)),
                   ("knapsack", (0, 1), sac_a_dos.Sac_A_Dos(self.display)),
                   ("exit",     (2, 1), "EXIT")]
        )
        
        self.menuButton = None
        self.helpButton = None
        self.solutionButton = None

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
                    if inAlgo:
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
                    button = event.button
                    pos = event.pos
                    
                    if inMenu and button == 1:
                        alg = self.menu.update(pos)
                        if alg != None:
                            algo = alg
                            inMenu = False
                            inAlgo = True
                            # prevent update for now
                            button = None

            # update
            if inAlgo and pos != (0, 0)\
                    and button != None:
                
                if self.buttonMenu.collidepoint(pos):
                    inAlgo = False
                    inMenu = True
                
                if self.buttonHelp.collidepoint(pos):
                    inAlgo = False
                    inHelp = True
                
                if self.buttonSolution.collidepoint(pos):
                    algo.show_solution = not algo.show_solution
                
                algo._update(pos, button)
            
            if inHelp and pos != (0, 0) and button is not None:
                if self.buttonMenu.collidepoint(pos):
                    inHelp = False
                    inAlgo = True

            # drawing's handling
            if inMenu:  # if we are inside the main menu
                self.menu.draw(self.display)
            elif inAlgo:  # else if we are inside an algorithm
                self.display.fill((1, 0, 0))  #temp fix : please use a backgrounf for your algo !
                # Add some buttons
                width, height = self.display.get_size()
                
                imgMenu = pygame.image.load('ui/pix/menu/back.png').convert_alpha()
                rectMenu = imgMenu.get_rect()
                rectMenu.bottom = height - 5
                rectMenu.left = 5
                self.buttonMenu = self.display.blit(imgMenu, rectMenu)
                
                imgHelp = pygame.image.load('ui/pix/menu/help.png').convert_alpha()
                rectHelp = imgHelp.get_rect()
                rectHelp.bottom = height - 5
                rectHelp.right = width - 155
                self.buttonHelp = self.display.blit(imgHelp, rectHelp)
                
                imgSolution = pygame.image.load('ui/pix/menu/solution.png').convert_alpha()
                rectSolution = imgSolution.get_rect()
                rectSolution.bottom = height - 5
                rectSolution.right = width - 5
                self.buttonSolution = self.display.blit(imgSolution, rectSolution)
                
                algo._draw()
            elif inHelp: # else if we are in a help screen
                self.display.fill((1, 0, 0))
                
                # back button
                width, height = self.display.get_size()
                
                imgMenu = pygame.image.load('ui/pix/menu/back.png').convert_alpha()
                rectMenu = imgMenu.get_rect()
                rectMenu.bottom = height - 5
                rectMenu.left = 5
                self.buttonMenu = self.display.blit(imgMenu, rectMenu)
                
                algo._help()
            pygame.display.flip()  # draw on display
            self.clock.tick(self.fpsLimit)  # limit the fps


if __name__ == '__main__':
    a = iutbm(800, 600)
    a.main()
