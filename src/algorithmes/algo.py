#!/bin/env python

import pygame

class algo:
	'''
		Classe abstraite representant un
		algorithme
	'''
	def __init__(self):
		pass

	def play(self):
		'''
			Permet au joueur d'essayer de resoudre
			le probleme pose
		'''
		raise NotImplementedError

	def solve(self):
		'''
			Resolution pas-a-pas du probleme
		'''
		raise NotImplementedError
	
	def explain(self):
		'''
			Petit texte explicatif/historique au sujet
			du probleme pose
		'''
		raise NotImplementedError
