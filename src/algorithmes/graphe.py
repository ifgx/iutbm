import random


class Graphe(object):
	def __init__(self, nbNoeuds, nbLiens, minPoids, maxPoids):
		self.graphe = []
		liste_noeuds = [Point(i) for i in xrange(nbNoeuds)]
		for i in xrange(nbLiens):
			noeud1 = random.choice(liste_noeuds)	
			noeud2 = random.choice(liste_noeuds)	
			poids = random.randint(minPoids, maxPoids)
			lien = Lien(noeud1, noeud2, poids) 
			self.graphe.append(lien)
	
	def ajout_lien(self, lien):
		if lien in self.graphe:
			#suppression du doublon
			self.graphe.pop(lien)
		self.graphe.append(lien)

	def supprime_lien(self, lien):
		if lien in self.graphe:
			self.graphe.pop(lien)
		else:  # FIXME
			raise
	
	def affiche(self):
		'''
			Affiche sur la sortie standard
			le graphe (debug)
		'''
		for i in self.graphe:
			print 'point1 : %s' % i.lien[0].nom
			print 'point2 : %s' % i.lien[1].nom
			print 'poids du lien : %s' % i.lien[2]
			print '\n'
		

class Point(object):
	def __init__(self, nom):
		self.nom = nom
		self.visite = False


class Lien(object):
	def __init__(self, sommet1, sommet2, poids):
		self.nom = str(sommet1.nom) + " - " + str(sommet2.nom)
		self.lien = (sommet1, sommet2, poids)


bleh = Graphe(10, 11, 1, 14)
bleh.affiche()
