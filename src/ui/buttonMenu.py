#-*-coding:utf8-*-

import pygame
import sys

class Menu:
    def __init__(self, choices):
        self.path = "ui/pix/menu/"
        
        #repere
        self.minx = 0.0
        self.maxx = 3.0
        self.miny = 0.0
        self.maxy = 2.0
        
        self.choices = choices
    
    def _get_corres_pixel(self, display, (x, y)):
        '''
            Get the corresponding pixel
            minx, maxx, miny, maxy are your repere's size
        '''
        width, height = display.get_size()
        posx = 64 + ((float(x) - self.minx) / (self.maxx - self.minx) * (width - 64))
        posy = 192 + ((float(y) - self.miny) / (self.maxy - self.miny) * (height - 190))
        return int(posx), int(posy)
    
    def draw(self, display):
        display.fill((30, 30, 30))
        
        grad = pygame.image.load(self.path + "grad.png").convert_alpha()
        for i in range(display.get_rect().width):
            display.blit(grad, (i, 0))
        
        title = pygame.image.load(self.path + "title.png").convert_alpha()
        titleRect = title.get_rect()
        titleRect.top = 16
        titleRect.centerx = display.get_rect().width / 2
        display.blit(title, titleRect)
        
        self.buttons = []
        
        for button, coords, algo in self.choices:
            image = pygame.image.load(self.path + button + ".png").convert_alpha()
            self.buttons.append((button, display.blit(image, self._get_corres_pixel(display, coords)), algo))
        
    
    def update(self, (x, y)):
        for nom, rect, algo in self.buttons:
            if rect.collidepoint(x, y):
                if algo == "EXIT":
                    sys.exit(0)
                else:
                    return algo
        return None
