#!/bin/env python

import algo
import pygame
import sys


class iutbm:
	'''
		Classe principale
	'''
	def __init__():
		self.w = window()

	def main():
		while True:
			self.w.screen.fill(black)
			pygame.display.flip()


class window:
	'''
		Fenetre principale
	'''
	def __init__(self):
		pygame.init()
		size = width, height = 800, 600
		self.screen = pygame.display.set_mode(size)


if __name__ == '__main__':
	a = iutbm
	a.main()
