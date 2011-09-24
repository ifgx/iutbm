import random


class Graphe(object):
	'''
		classe representant un graphe
	'''
	def __init__(self, nbNoeuds, nbLiens, minPoids, maxPoids):
		if nbNoeuds > nbLiens - 1:  # graphe non connexe
			raise
		elif minPoids < 0:  # poids negatif
			raise
		elif maxPoids == float('inf'):  # poids infini
			raise
		elif minPoids > maxPoids:  # PIGNOUF !
			raise
		elif nbNoeuds < 1:  # pas de sommets
			raise
		elif nbLiens < 1:  # pas de liens
			raise

		self.liste_liens = []
		self.liste_sommets = [Sommet(i) for i in xrange(nbNoeuds)]
		for i in xrange(nbLiens):
			sommet1 = random.choice(self.liste_sommets)
			sommet2 = random.choice(self.liste_sommets)
			poids = random.randint(minPoids, maxPoids)
			lien = Lien(sommet1, sommet2, poids)
			self.liste_liens.append(lien)

		self.debut = random.choice(self.liste_sommets)
		self.fin = random.choice(self.liste_sommets)

	def ajout_lien(self, lien):
		'''
			inutile
		'''
		if lien in self.graphe:
			#suppression du doublon
			self.graphe.pop(lien)
		self.graphe.append(lien)

	def supprime_lien(self, lien):
		'''
			inutile
		'''
		if lien in self.graphe:
			self.graphe.pop(lien)
		else:  # FIXME
			raise

	def affiche(self):
		'''
			affiche sur la sortie standard le graphe (debug)
		'''
		print('debut : %s' % self.debut.nom)
		print('fin : %s\n' % self.fin.nom)
		for i in self.graphe:
			print('point : %s' % i.sommet1.nom)
			print('point : %s' % i.sommet2.nom)
			print('poids : %s\n' % i.poids)

	def plus_proche_voisin(self, sommet):
		'''
			retourne le lien menant au plus proche voisin
			non visite du sommet donne
		'''
		minimum = float('inf')
		proche_sommet = Sommet()
		for i in self.liste_liens:
			if i.sommet1 == sommet:
				if i.poids < minimum and i.sommet2.visite is False:
					minimum = i.poids
					proche_sommet = i.sommet2
			elif i.sommet2 == sommet:
				if i.poids < minimum and i.sommet1.visite is False:
					minimum = i.poids
					proche_sommet = i.sommet1
		return proche_sommet

class Sommet:
	'''
		classe representant un sommet du graphe
	'''
	def __init__(self, nom=''):
		self.nom = nom
		self.visite = False
		self.score = float('inf')

	def affiche(self):
		print self.nom
		print 'visite: %s' % self.visite
		print 'score: %s\n' % self.score


class Lien(object):
	'''
		classe representant un lien entre deux sommets
	'''
	def __init__(self, sommet1='', sommet2='', poids=float('inf')):
		self.sommet1 = sommet1
		self.sommet2 = sommet2
		self.poids = poids
		self.visite = False

	def affiche(self):
		print str(self.sommet1) + ':' + str(self.sommet2) + ' (' + str(self.poids) + ')' + str(self.visite) + '\n'

#bleh = Graphe(10, 11, 1, 14)
#bleh.affiche()
