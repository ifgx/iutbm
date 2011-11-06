import pygame

class Algo:
    '''
        Abstract class which represent
        an algorithm
    '''
    def __init__(self, display):
        self.display = display
        self.font = pygame.font.Font(None, 17)
        self.text = 'generic algo'
        self.description = 'algorithm\'s description'

    def _solve(self, ):
        '''
            Solve the problem
        '''
        raise NotImplementedError

    def _explain(self):
        '''
            Display a short explaination text
        '''
        text = self.font.render(self.text, True, (255, 0, 0))
        self.display.blit(text, (10, 10))
        text = self.font.render(self.description, True, (255, 0, 0))
        self.display.blit(text, (10, 30))

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
