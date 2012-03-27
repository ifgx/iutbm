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
        
        self.show_solution = False

    def _solve(self, ):
        '''
            Solve the problem
        '''
        raise NotImplementedError


    def _help(self):
        '''
            Display an helping text
        '''
        # display "text"
        self.nameFont = pygame.font.Font('freesansbold.ttf', 40)
        text = self.nameFont.render(self.text, True, (255, 0, 0))
        self.display.blit(text, (10, 10))

        # display "description" with carriage return on "#"
        self.descFont = pygame.font.Font(None, 25)
        for cpt, line in enumerate(self.description.split('#')):
            text = self.descFont.render(line, True, (255, 255, 255))
            self.display.blit(text, (10, 25 * cpt + 80))


        text_1 = self.descFont.render("select", True, (255, 0, 0))
        rect_1 = text_1.get_rect()
        rect_1.center = self._get_corres_pixel(35,70)
        self.display.blit(text_1, rect_1)

        text_1 = self.descFont.render("cancel", True, (255, 0, 0))
        rect_1 = text_1.get_rect()
        rect_1.center = self._get_corres_pixel(65,70)
        self.display.blit(text_1, rect_1)

        text_1 = pygame.image.load("ui/pix/help/clic-right.jpg")
        rect_1 = text_1.get_rect()
        rect_1.center = self._get_corres_pixel(65,80)
        self.display.blit(text_1, rect_1)

        text_1 = pygame.image.load("ui/pix/help/clic-left.jpg")
        rect_1 = text_1.get_rect()
        rect_1.center = self._get_corres_pixel(35,80)
        self.display.blit(text_1, rect_1)

    def _get_corres_pixel(self, x, y):
        '''
            Get the corresponding pixel
            minx, maxx, miny, maxy are your repere's size
        '''
        width, height = self.display.get_size()
        posx = (float(x) - self.minx) / (self.maxx - self.minx) * width
        posy = (float(y) - self.miny) / (self.maxy - self.miny) * height
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
