#!/bin/env python

import pygame
import sys
import math

#import ui
from ui import rotatingMenu as rM
#import algorithmes
from algorithmes import voyage

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

	# tableau des algos
	self.drawalgo = ['QUIT', voyage.Voyage(self.display),
		'FIXME', 'FIXME', 'FIXME', 'FIXME']

        # a propos de la fenetre
        pygame.display.set_caption('IUTBM')

        #initialisation du menu
        self.menu = rM.RotatingMenu(x=320, y=240, radius=220, arc=math.pi,
                defaultAngle=math.pi/2.0)
        items = ['quit', 'saleman traveller', 'plus court chemin',
                'couplage', 'sac a dos', 'confiserie']
        [self.menu.addItem(rM.MenuItem(i)) for i in items]
        self.menu.selectItem(0)

    def main(self):
	inMenu = True
	intExplain = False
        while True:
            #gestion des evenements
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
		elif event.type == pygame.KEYDOWN:
		    if inMenu:  # si nous sommes dans le menu
			if event.key == pygame.K_LEFT:
			    self.menu.selectItem(self.menu.selectedItemNumber + 1)
			elif event.key == pygame.K_RIGHT:
			    self.menu.selectItem(self.menu.selectedItemNumber - 1)
			elif event.key == pygame.K_UP:  # selection de l'item du menu
			    if self.menu.selectedItemNumber == 0:  # Item "quit"
				sys.exit(0)
			    else:
				algo = self.drawalgo[self.menu.selectedItemNumber]
				inMenu = False
				inAlgo = True
		    if event.key == pygame.K_ESCAPE:
			if inMenu:
				sys.exit(0)
			elif inAlgo:  # si nous sommes dans un algo
				inMenu = True
				inAlgo = False
			elif inHelp:  # si nous sommes dans l'aide
				inAlgo = True

            # mis a jour
	    if inMenu:
		self.menu.update()

            #dessin
            self.display.fill((0, 0, 0)) # fond noir
	    if inMenu:
		self.menu.draw(self.display)
	    elif inAlgo:
		algo._draw()
            pygame.display.flip()
            self.clock.tick(self.fpsLimit)


if __name__ == '__main__':
    a = iutbm(800, 600)
    a.main()
