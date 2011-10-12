import pygame

class Algo:
	'''
		Classe abstraite representant un
		algorithme
	'''
	def __init__(self, display):
		self.display = display
		self.font = pygame.font.Font(None, 17)

	def play(self):
		'''
			Permet au joueur d'essayer de resoudre
			le probleme pose
		'''
		self._play()

	def solve(self):
		'''
			Resolution pas-a-pas du probleme
		'''
		self._solve()

	def explain(self):
		'''
			Petit texte explicatif/historique au sujet
			du probleme pose : il est affiche
			AVANT que le jeu commence.
		'''
		self._explain()

	def _play(self):
		raise NotImplementedError

	def _solve(self):
		raise NotImplementedError

	def _explain(self):
		raise NotImplementedError
