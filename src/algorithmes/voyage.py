#!/bin/env python

import logging
import random
import math

import graphe
import algo

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

		matrix = []
		matrix.append('MATRIX')
		for i in xrange(nbpoints):
			x = random.randint(minx, maxx)
			y = random.randint(miny, maxy)
			matrix.append([i, x, y])
		matrix[0] = [i for i in matrix]

