'''
    Traveler saleman's problem
'''

import random
import math
import pygame

import graphe
import algo


class Sommet:
    '''
        Implement a "point"/"summit"
    '''
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = x
        self.y = y
        self.visite = False

    def __repr__(self):
        return str(self.nom)


class Voyage(algo.Algo):
    '''
        Traveler saleman's problem
    '''
    def __init__(self, display):
        algo.Algo.__init__(self, display)
        nbpoints = 10
        self.minx = 0.0
        self.maxx = 10.0
        self.miny = 0.0
        self.maxy = 10.0
        self.matrix = self._create_matrix(nbpoints, self.minx, self.maxx,
                self.miny, self.maxy)
        self.text = 'Voyageur de commerce'
        self.first_som = 1

        #lenght of the path
        self.computed_len = self.user_len = 0

        #path
        self.computed_path = self.user_path = []

        # draw's variables
        self.selected = None
        self.nbselected = 0
        self.lines = []

    def __repr__(self):
        return '\n'.join([str(i) for i in self.matrix])

    def _create_matrix(self, nbpoints, minx, maxx, miny, maxy):
        '''
            return a matrix like :
                T 1 2 3 4 ... nbpoints
                1 0 d d d ...
                2 d 0 d d
                3 d d 0 d
                4 d d d 0

            with:
                T = number of lines
                d = distance between two correspondings points
        '''
        #creation of the matrix
        matrix = [[0 for i in xrange(nbpoints)] for j in xrange(nbpoints)]

        #fill the first row and first col with points
        for cpt in xrange(nbpoints):
            x = random.randint(minx, maxx)
            y = random.randint(miny, maxy)
            matrix[0][cpt] = matrix[cpt][0] = Sommet(cpt, x, y)
        matrix[0][0] = nbpoints - 1

        #compute the distances between all the points
        for i in xrange(nbpoints - 1):
            for j in xrange(nbpoints - 1):
                if i != j:
                    ip = i + 1
                    jp = j + 1
                    x1 = matrix[0][ip].x
                    y1 = matrix[0][ip].y
                    x2 = matrix[jp][0].x
                    y2 = matrix[jp][0].y
                    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
                    matrix[ip][jp] = distance
        return matrix

    def _reset(self):
        '''
            Reset the graph to a 'clean' state
        '''
        for i in xrange(self.matrix[0][0]):
            self.matrix[0][i + 1].visite = False
            self.matrix[i + 1][0].visite = False

    def _solve(self, ligne=1):  # the first point is the first of the matrix
        '''
            Resolution a grand coup de plus proche voisin !
        '''
        if ligne > self.matrix[0][0] or 0 > ligne:  # invalid start point
            raise IndexError
        self.computed_path = [self.matrix[0][ligne], ]
        self.matrix[0][ligne].visite = True  # le premier point est visite

        tmp = -1
        for i in xrange(1, self.matrix[0][0]):
            minimum = float('inf')
            for j in xrange(1, self.matrix[0][0] + 1):
                # parcourt de la ligne a la recherche du plus proche point non parcouru
                if 0 < self.matrix[ligne][j] < minimum and self.matrix[0][j].visite is False:
                    # Si le point est plus proche que tout ce
                    # qu'on a trouve jusqu'a present
                    # et qu'il est non marque, marquons le comme le plus proche
                    minimum = self.matrix[ligne][j]
                    tmp = j
            if minimum != float('inf'):
                self.computed_path.append(self.matrix[0][tmp])  # on ajoute le point trouve au chemin
                self.matrix[0][tmp].visite = True  # et on le marque come parcouru
                self.computed_len += minimum  # on ajoute la distance parcourue a la distance totale
                ligne = tmp
        self.computed_len += self.matrix[1][tmp]
        #self.computed_path.append(self.matrix[0][tmp])
        self._reset()

    def _get_corres_pixel(self, x, y):
        '''
            Get the corresponding pixel
        '''
        width, height = self.display.get_size()
        posx = (x - self.minx) / (self.maxx - self.minx) * width
        posy = (y - self.miny) / (self.maxy - self.miny) * height
        return int(posx), int(posy)

    def _draw(self):
        width, height = self.display.get_size()

        for point in self.matrix[0][1:]:  # draw points
            pygame.draw.circle(self.display, (255, 0, 0), self._get_corres_pixel(point.x, point.y), 10, 0)

        if len(self.user_path) > 0:  # if the user has selected more than 1 point
            for i in xrange(len(self.user_path) - 1):  # draw user's path
                x, y = self._get_corres_pixel(self.user_path[i].x, self.user_path[i].y)
                x1, y1 = self._get_corres_pixel(self.user_path[i + 1].x, self.user_path[i + 1].y)
                pygame.draw.line(self.display, (255, 0, 0), (x, y), (x1, y1), 5)

        if self.nbselected == self.matrix[0][0]:  # if all points have been selected
            last = self.matrix[0][0] - 1
            for i in xrange(last):  # draw the computed path
                x, y = self._get_corres_pixel(self.computed_path[i].x, self.computed_path[i].y)
                x1, y1 = self._get_corres_pixel(self.computed_path[i + 1].x, self.computed_path[i + 1].y)
                pygame.draw.line(self.display, (0, 255, 0), (x, y), (x1, y1))

            #raccord the user's path first point to the last one
            x, y = self._get_corres_pixel(self.computed_path[0].x, self.computed_path[0].y)
            x1, y1 = self._get_corres_pixel(self.user_path[last].x, self.user_path[last].y)
            pygame.draw.line(self.display, (255, 0, 0), (x, y), (x1, y1), 5)

            # raccord first compted'spath selected point to the last one
            x1, y1 = self._get_corres_pixel(self.computed_path[last].x, self.computed_path[last].y)
            pygame.draw.line(self.display, (0, 255, 0), (x, y), (x1, y1))

        #user's length
        text = self.font.render('User: ' + str(self.user_len), True, (255, 0, 0))
        self.display.blit(text, (10, 10))

        #computed lenght
        text = self.font.render('Computed: ' + str(self.computed_len), True, (255, 0, 0))
        self.display.blit(text, (10, 20))

    def _update(self, (x, y)):
        # detection of a click inside a circle
        index = 0
        for cpt, point in enumerate(self.matrix[0][1:]):
            real_x, real_y = self._get_corres_pixel(point.x, point.y)
            if real_x - 10 < x < real_x + 10 and real_y - 10 < y < real_y + 10:
                index = cpt + 1
                break

        if index:  # if the click is on a circle
            if self.selected is None:
                self.first_som = index
                self.nbselected += 1
                self.matrix[0][index].visite = True
                self.selected = self.matrix[0][index]
                self._solve(self.matrix[0][index].nom)  # compute the optimal solution
                self.user_path.append(self.matrix[0][index])
            elif self.matrix[0][index].visite is False:
                self.user_len += self.matrix[index][self.selected.nom]  # incrementation of the lenght
                self.user_path.append(self.matrix[0][index])
                self.nbselected += 1
                self.matrix[0][index].visite = True
                self.selected = self.matrix[0][index]
            if len(self.user_path) == self.matrix[0][0]:  # if every points have been selected
                self.user_len += self.matrix[index][self.first_som]  # add the distance between first and last point
