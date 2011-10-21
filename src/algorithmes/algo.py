import pygame

class Algo:
	'''
		Abstract class which represent
		an algorithm
	'''
	def __init__(self, display):
		self.display = display
		self.font = pygame.font.Font(None, 17)

	def _solve(self):
		'''
			Solve the problem
		'''
		raise NotImplementedError

	def _explain(self):
		'''
			Display a short explaination text
		'''
		raise NotImplementedError
	
	def _reset(self):
		'''
			Reset a problem
		'''
		pass
	
	def _draw(self):
		'''
			Draw the current state of the problem
		'''
		raise NotImplementedError
		
	def _update(self, (x, y)):
		'''
			Update the state of the problem:
			this method is called only on mouse click.
			(FIXME : call this method every frames ?)
			x and y represent the position of
			the mouse click.
		'''
		raise NotImplementedError
