#!/bin/env python

import logging
import random
import math

import graphe
import algo

class Sommet:
	def __init__(self, nom, x, y):
		self.nom = nom
		self.x = x
		self.y = y
		self.visite = False

	def __repr__(self):
		return str(self.nom)

class Voyage(algo.algo):
	'''
		Probleme du voyageur de commerce
	'''
	def __init__(self):
		nbpoints = 10
		minx = 0
		maxx = 10
		miny = 0
		maxy = 10
		self.matrix = self._create_matrix(nbpoints, minx, maxx, miny, maxy)


	def __repr__(self):
		return '\n'.join([str(i) for i in self.matrix])

	def _create_matrix(self, nbpoints, minx, maxx, miny, maxy):
		'''
			retourne un matrice de la forme:
				T 1 2 3 4 ... nbpoints
				1 0 d d d ...
				2 d 0 d d
				3 d d 0 d
				4 d d d 0
			
			avec:
				T = nombre de lignes
				d = distance entre les deux points
					correspondants
		'''
		matrix = [[0 for i in xrange(nbpoints)] for j in xrange(nbpoints)]

		for cpt in xrange(nbpoints):
			x = random.randint(minx, maxx)
			y = random.randint(miny, maxy)
			matrix[0][cpt] = Sommet(cpt, x, y) 
			matrix[cpt][0] = Sommet(cpt, x, y) 
		matrix[0][0] = nbpoints - 1

		for i in xrange(nbpoints - 1):
			for j in xrange(nbpoints - 1):
				if i != j:
					x1 = matrix[0][i+1].x
					y1 = matrix[0][i+1].y
					x2 = matrix[j+1][0].x
					y2 = matrix[j+1][0].y
					distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
					matrix[i+1][j+1] = distance 
					#matrix[i+1][j+1] = int(distance) #debug

		return matrix

	def _solve(self, ligne=1):  # le premier point est le 1 par defaut
		if ligne > self.matrix[0][0] or 0 > ligne:
			raise IndexError
		chemin = [ligne, ]
		self.matrix[0][ligne].visite = True  # le premier point est visite

		for i in xrange(self.matrix[0][0] - 1):
			minimum = float('inf')
			tmp = -1
			for j in xrange(1, self.matrix[0][0]):
				# parcourt de la ligne a la recherche du plus proche point non parcouru
				if 0 < self.matrix[ligne][j] < minimum and self.matrix[0][j].visite is False:
					# Si le point est plus proche que tout ce
					# qu'on a trouve jusqu'a present
					# et qu'il est non marque, marquons le comme le plus proche
					minimum = self.matrix[ligne][j]
					tmp = j
			chemin.append(self.matrix[0][tmp])  # on ajoute le point trouve au chemin
			self.matrix[0][tmp].visite = True  # et on le marque come parcouru
			ligne = tmp
		return chemin

b = Voyage()
#print b._solve()
#print'\n'
#print b
