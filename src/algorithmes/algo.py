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
		self._play()

	def solve(self):
		'''
			Resolution pas-a-pas du probleme
		'''
		self._solve()
	
	def explain(self):
		'''
			Petit texte explicatif/historique au sujet
			du probleme pose : il est affiche
			AVANT que le jeu commence.
		'''
#L'ideal serait une belle zone texte, avec un bete texte intrinseque
#a chaque algo a balancer dedans
		self._explain()

	def _play(self):
		raise NotImplementedError
		
	def _solve(self):
		raise NotImplementedError

	def _explain(self):	
		raise NotImplementedError
