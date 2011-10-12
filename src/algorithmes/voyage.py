#!/bin/env python

import logging
import random
import math
import sys
import pygame

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

class Voyage(algo.Algo):
	'''
		Probleme du voyageur de commerce
	'''
	def __init__(self, display):
		algo.Algo.__init__(self, display)
		nbpoints = 10
		self.minx = 0.0
		self.maxx = 10.0
		self.miny = 0.0
		self.maxy = 10.0
		self.matrix = self._create_matrix(nbpoints, self.minx, self.maxx, self.miny, self.maxy)
		self.text = 'Voyageur de commerce'
		self.distance = 0
		self.first_som = 1

		# draw's variables
		self.selected = None
		self.nbselected = 0
		self.lines = []

		# solve on start
		#self.lenght = self._solve(self.first_som)
		self._reset()

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
		#creation of the matrix
		matrix = [[0 for i in xrange(nbpoints)] for j in xrange(nbpoints)]

		#fill the first row and first col with points
		for cpt in xrange(nbpoints):
			x = random.randint(minx, maxx)
			y = random.randint(miny, maxy)
			matrix[0][cpt] = matrix[cpt][0] = Sommet(cpt, x, y)
		matrix[0][0] = nbpoints - 1

		#compute the distances between all the points
		for i in xrange(nbpoints - 1):
			for j in xrange(nbpoints - 1):
				if i != j:
					x1 = matrix[0][i+1].x
					y1 = matrix[0][i+1].y
					x2 = matrix[j+1][0].x
					y2 = matrix[j+1][0].y
					distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
					#matrix[i+1][j+1] = distance
					matrix[i+1][j+1] = int(distance) #debug
		return matrix

	def _reset(self):
		for i in xrange(self.matrix[0][0]):
			#reset du graphe
			self.matrix[0][i + 1].visite = False
			self.matrix[i + 1][0].visite = False
	def _solve(self, ligne=1):  # le premier point est le 1 par defaut
		'''
			Resolution a grand coup de plus proche voisin !
		'''
		if ligne > self.matrix[0][0] or 0 > ligne:
			raise IndexError
		chemin = [ligne, ]
		self.matrix[0][ligne].visite = True  # le premier point est visite
		self.distance = 0

		tmp = -1
		for i in xrange(1, self.matrix[0][0]):
			minimum = float('inf')
			for j in xrange(1, self.matrix[0][0] + 1):
				# parcourt de la ligne a la recherche du plus proche point non parcouru
				if 0 < self.matrix[ligne][j] < minimum and self.matrix[0][j].visite is False:
					# Si le point est plus proche que tout ce
					# qu'on a trouve jusqu'a present
					# et qu'il est non marque, marquons le comme le plus proche
					minimum = self.matrix[ligne][j]
					tmp = j
			if minimum != float('inf'):
				chemin.append(self.matrix[0][tmp])  # on ajoute le point trouve au chemin
				self.matrix[0][tmp].visite = True  # et on le marque come parcouru
				self.distance += minimum  # on ajoute la distance parcourue a la distance totale
				ligne = tmp
		self.distance += self.matrix[1][tmp]
		return chemin

	def _get_corres_pixel(self, pos):
		width, height = self.display.get_size()
		x = (pos[0] - self.minx) / (self.maxx - self.minx) * width
		y = (pos[1] - self.miny) / (self.maxy - self.miny) * height
		return int(x), int(y)

	def _draw(self):
		width, height = self.display.get_size()
		for point in self.matrix[0][1:]:
			pos = (point.x, point.y)
			pygame.draw.circle(self.display, (255, 0, 0), self._get_corres_pixel(pos), 10, 0)
		for line in self.lines:
			pygame.draw.line(self.display, (255, 0, 0), line[0], line[1])
		text = self.font.render(str(self.distance), True, (255, 0, 0))
		self.display.blit(text, (10, 10))

	def _update(self, (x, y)):
		# detection of a click inside a circle
		index = 0
		for cpt, point in enumerate(self.matrix[0][1:]):
			real_x, real_y = self._get_corres_pixel((point.x, point.y))
			if real_x - 10 < x < real_x + 10 and real_y - 10 < y <real_y + 10:
				index = cpt + 1
				break

		if index:  # if the click is on a circle
			if self.selected is None:
				self.first_som = index
				self.nbselected += 1
				self.matrix[0][index].visite = True
				self.selected = self.matrix[0][index]
				# compute the optimal solution
				#self._solve(self.matrix[0][index].nom)
			elif self.matrix[0][index].visite is False:
				self.distance += self.matrix[index][self.selected.nom]  # incrementation of the lenght
				x1, y1 = self._get_corres_pixel((self.selected.x, self.selected.y))
				self.lines.append(((x1, y1), (x, y)))
				self.nbselected += 1
				self.matrix[0][index].visite = True
				self.selected = self.matrix[0][index]

		if self.nbselected == self.matrix[0][0]:  # if all points have been selected
			distance = self.distance
			self._solve(self.first_som)
			print "distance trouveee: " + str(distance)
			print "distance calculee: " + str(self.distance)
			sys.exit(0)
