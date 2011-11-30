'''
    File for generic stuffs
'''

import pygame


class Algo:
    '''
        Abstract class which represent
        an algorithm
    '''
    def __init__(self, display):
        self.display = display
        self.font = pygame.font.Font(None, 17)

        #help screen
        self.text = 'generic algo'
        self.description = 'algorithm\'s description# for a carriage return#>o_/'

        #repere
        self.minx = 0.0
        self.maxx = 100.0
        self.miny = 0.0
        self.maxy = 100.0

    def _solve(self, ):
        '''
            Solve the problem
        '''
        raise NotImplementedError

    def _explain(self):
        '''
            Display a short explaination text
        '''
        # display "text"
        text = self.font.render(self.text, True, (255, 0, 0))
        self.display.blit(text, (10, 10))

        # display "description" with carriage return on "#"
        for cpt, line in enumerate(self.description.split('#')):
            text = self.font.render(line, True, (255, 0, 0))
            self.display.blit(text, (10, 10 * cpt + 30))

    def _get_corres_pixel(self, x, y):
        '''
            Get the corresponding pixel
            minx, maxx, miny, maxy are your repere's size
        '''
        width, height = self.display.get_size()
        posx = (x - self.minx) / (self.maxx - self.minx) * width
        posy = (y - self.miny) / (self.maxy - self.miny) * height
        return int(posx), int(posy)

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
            x and y represent the position of
            the mouse click.
        '''
        raise NotImplementedError
