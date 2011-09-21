#!/bin/env python

import graphe

class Voyage(algo):
	'''
		Probleme du voyageur de commerce
	'''
	def __init__(self):
		self.graphe = graphe.Graphe(10, 20, 1, 10)
	
	def _solve(self):
		liste_liens = []  # liste ordonnee des liens a parcourir
		sommet_actuel = self.debut
		for i in self.liste_noeuds:
			liste_lien.append(sommet_actuel)
			sommet_actuel.visite = True
			sommet_actuel = plus_proche_voisin(sommet_actuel)

