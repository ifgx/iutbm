import random


class Graphe(object):
	'''
		classe representant un graphe
	'''
	def __init__(self, nbNoeuds, nbLiens, minPoids, maxPoids):
		#TODO : verification des valeurs
		self.graphe = []
		self.liste_sommets = [Sommet(i) for i in xrange(nbNoeuds)]
		for i in xrange(nbLiens):
			sommet1 = random.choice(self.liste_sommets)	
			sommet2 = random.choice(self.liste_sommets)	
			poids = random.randint(minPoids, maxPoids)
			lien = Lien(sommet1, sommet2, poids) 
			self.graphe.append(lien)
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
			du sommet donne
		'''
		minimum = float('inf')
		lien = Lien()
		for i in self.graphe:
			if i.sommet1 == sommet or i.sommet2 == sommet:
				if i.poids < minimum:
					minimum = i.poids
					lien = i
		return lien

		

class Sommet(object):
	'''
		classe representant un sommet du graphe
	'''
	def __init__(self, nom):
		self.nom = nom
		self.visite = False
		self.score = float('inf')


class Lien(object):
	'''
		classe representant un lien entre deux sommets
	'''
	def __init__(self, sommet1='', sommet2='', poids=float('inf')):
		self.sommet1 = sommet1
		self.sommet2 = sommet2
		self.poids = poids
		self.visite = False

#bleh = Graphe(10, 11, 1, 14)
#bleh.affiche()
