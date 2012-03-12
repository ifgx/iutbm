#!/usr/bin/env python

'''
    Complexity sensibilisation application
'''

import pygame
import sys

import ui.theme as theme
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

        # initialisation of the menu
        self.menu = bM.Menu(
                  [("salesman", (0, 0), voyage.Voyage(self.display)),
                   ("shortest", (1, 0), plus_court.Graphe(self.display)),
                   ("coupling", (2, 0), couplage.Couplage(self.display)),
                   ("knapsack", (0, 1), sac_a_dos.Sac_A_Dos(self.display)),
                   ("exit",     (2, 1), "EXIT")]
        )

        self.buttonMenu = None
        self.buttonHelp = None
        self.buttonSolution = None

        self.inMenu = True
        self.inAlgo = False
        self.inHelp = False

        self.algo = None

    def main(self):
        while True:  # Main loop
            button = None
            pos = (0, 0)  # reset saved mouse's position
            events = pygame.event.get()  # events handling
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)  # quit the game
                elif event.type == pygame.KEYDOWN:
                    if self.inAlgo:
                        if event.key == pygame.K_h:
                            #h is the help key
                            self.inHelp = True
                            self.inAlgo = False

                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        # The escape and q key are bind to action INSIDE and OUTSIDE the menu
                        if self.inMenu:
                            sys.exit(0)  # quit the game
                        elif self.inAlgo:  # if we are inside an algo
                            self.inMenu = True
                            self.inAlgo = False
                        elif self.inHelp: # if we are inside a helpscreen
                            self.inAlgo = True
                            self.inHelp = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button = event.button
                    pos = event.pos

                    if self.inMenu and button == 1:
                        selected_algo = self.menu.update(pos)
                        if selected_algo:
                            self.algo = selected_algo
                            self.inMenu = False
                            self.inAlgo = False
                            self.inHelp = True
                            # reset algo
                            self.algo.__init__(self.display)
                            # prevent update for now
                            button = None

            # Button's handling inAlgo
            if self.inAlgo and pos and button:
                if self.buttonMenu.collidepoint(pos):
                    self.inAlgo = False
                    self.inMenu = True
                elif self.buttonHelp.collidepoint(pos):
                    self.inAlgo = False
                    self.inHelp = True
                elif self.buttonSolution.collidepoint(pos):
                    self.algo.show_solution = not self.algo.show_solution
                self.algo._update(pos, button)

            self._drawHandling(pos, button)
            pygame.display.flip()  # draw on display
            self.clock.tick(self.fpsLimit)  # limit the fps

    def _drawHandling(self, pos, button):
        '''
            Drawing's handling
        '''
        if self.inMenu:  # if we are inside the main menu
            self.menu.draw(self.display)
        elif self.inAlgo:  # else if we are inside an algorithm
            self._drawInAlgo()
        elif self.inHelp: # else if we are in a help screen
            if pos and button and self.buttonMenu.collidepoint(pos):
                self.inHelp = False
                self.inAlgo = True
            else:
                self._drawInHelp()

    def _drawInHelp(self):
        self.display.fill((1, 0, 0))

        # back button
        width, height = self.display.get_size()

        # FIXME : "go to game" instead of "back" ty
        img_menu = pygame.image.load('ui/pix/menu/back.png').convert_alpha()
        rect_menu = img_menu.get_rect()
        rect_menu.bottom = height - 5
        rect_menu.left = 5
        self.buttonMenu = self.display.blit(img_menu, rect_menu)

        self.algo._help()

    def _drawInAlgo(self):
        self.display.fill((1, 0, 0))  #temp fix : please use a backgrounf for your algo !
        # Add some buttons
        width, height = self.display.get_size()

        img_menu = pygame.image.load('ui/pix/menu/back.png').convert_alpha()
        rect_menu = img_menu.get_rect()
        rect_menu.bottom = height - 5
        rect_menu.left = 5
        self.buttonMenu = self.display.blit(img_menu, rect_menu)

        img_help = pygame.image.load('ui/pix/menu/help.png').convert_alpha()
        rect_help = img_help.get_rect()
        rect_help.bottom = height - 5
        rect_help.right = width - 155
        self.buttonHelp = self.display.blit(img_help, rect_help)

        img_solution = pygame.image.load('ui/pix/menu/solution.png').convert_alpha()
        rect_solution = img_solution.get_rect()
        rect_solution.bottom = height - 5
        rect_solution.right = width - 5
        self.buttonSolution = self.display.blit(img_solution, rect_solution)

        self.algo._draw()



if __name__ == '__main__':
    a = iutbm(800, 600)
    a.main()
