#!/bin/env python

import graphe
import algo

class Voyage(algo.algo):
	'''
		Probleme du voyageur de commerce
	'''
	def __init__(self):
		self.graphe = graphe.Graphe(10, 20, 1, 10)
	
	def _solve(self):
		liste_sommets = []  # liste ordonnee des sommets a parcourir
		sommet_actuel = self.graphe.debut
		for i in self.graphe.liste_sommets:
			liste_sommets.append(sommet_actuel)
			sommet_actuel.visite = True
			sommet_actuel = self.graphe.plus_proche_voisin(sommet_actuel)
		for i in liste_sommets:
			i.affiche()

b = Voyage()
#b.graphe.affiche()
b._solve()

