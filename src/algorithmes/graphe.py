import random


class Graphe(object):
	'''
		Classe representant un graphe
	'''
	def __init__(self, nbNoeuds, nbLiens, minPoids, maxPoids):
		self.graphe = []
		liste_noeuds = [Sommet(i) for i in xrange(nbNoeuds)]
		for i in xrange(nbLiens):
			noeud1 = random.choice(liste_noeuds)	
			noeud2 = random.choice(liste_noeuds)	
			poids = random.randint(minPoids, maxPoids)
			lien = Lien(noeud1, noeud2, poids) 
			self.graphe.append(lien)
	
	def ajout_lien(self, lien):
		'''
			Inutile
		'''
		if lien in self.graphe:
			#suppression du doublon
			self.graphe.pop(lien)
		self.graphe.append(lien)

	def supprime_lien(self, lien):
		'''
			Inutile
		'''
		if lien in self.graphe:
			self.graphe.pop(lien)
		else:  # FIXME
			raise
	
	def affiche(self):
		'''
			Affiche sur la sortie standard le graphe (debug)
		'''
		for i in self.graphe:
			print('point : %s' % i.sommet1.nom)
			print('point : %s' % i.sommet2.nom)
			print('poids : %s\n' % i.poids)
		

class Sommet(object):
	'''
		Classe representant un sommet du graphe
	'''
	def __init__(self, nom):
		self.nom = nom
		self.visite = False


class Lien(object):
	'''
		Classe representant un lien entre deux sommets
	'''
	def __init__(self, sommet1, sommet2, poids):
		self.sommet1 = sommet1
		self.sommet2 = sommet2
		self.poids = poids
		self.visite = False


#bleh = Graphe(10, 11, 1, 14)
#bleh.affiche()
