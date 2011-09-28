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

		#matrix = [['0']*nbpoints]*nbpoints  # FIXME
		matrix = [[0 for i in xrange(nbpoints)] for j in xrange(nbpoints)]

		for cpt in xrange(nbpoints):
			x = random.randint(minx, maxx)
			y = random.randint(miny, maxy)
			matrix[0][cpt] = Sommet(cpt, x, y) #[cpt, x, y]
			matrix[cpt][0] = Sommet(cpt, x, y) #[cpt, x, y]
		matrix[0][0] = ''


		for i in xrange(nbpoints - 1):
			for j in xrange(nbpoints - 1):
				if i != j:
					x1 = matrix[0][i+1].x#[1]
					y1 = matrix[0][i+1].y#[2]
					x2 = matrix[j+1][0].x#[1]
					y2 = matrix[j+1][0].y#[2]
					distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
					matrix[i+1][j+1] = int(distance) #debug

		for i in matrix:
			print i

b = Voyage()

