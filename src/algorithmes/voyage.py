'''
    Traveler saleman's problem
'''

import random
import math
import pygame

import algorithmes.algo
import ui.theme as theme


class Sommet:
    '''
        Implement a "point"/"summit"
    '''
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.visite = False

    def __repr__(self):
        return str(self.name)


class Voyage(algorithmes.algo.Algo):
    '''
        Traveler saleman's problem
    '''
    def __init__(self, display):
        algorithmes.algo.Algo.__init__(self, display)
        nbpoints = 10
        self.minx = 0.0
        self.maxx = 100.0
        self.miny = 0.0
        self.maxy = 100.0
        self.matrix = self._create_matrix(nbpoints)
        self.text = 'Travelling saleman problem'
        self.description = 'Given a list of cities and their\
pairwise distances,# the task is to find a shortest possible\
tour that visits each city exactly once.#\
It is a special case of the Traveling purchaser problem.#'
        self.first_som = -1  # will be set later

        #lenght of the path
        self.computed_len = self.user_len = 0

        #path
        self.computed_path = self.user_path = []

        # draw's variables
        self.selected = None
        self.nbselected = 0  # nb of user's selected points
        self.lines = []
        rect = pygame.image.load(theme.cities[0]).get_rect()
        self.hack_x = rect[2] / 2
        self.hack_y = rect[3] / 2

    def __repr__(self):
        return '\n'.join([str(i) for i in self.matrix])

    def _create_matrix(self, nbpoints):
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
        minx = self.minx * 0.9
        maxx = self.maxx * 0.9
        miny = self.miny * 0.9
        maxy = self.maxy * 0.9
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
                    distance = math.sqrt(math.pow(x2 - x1, 2)
                            + math.pow(y2 - y1, 2))
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
            Fill self.computed_len
            Fill self.computed_path with points

            Nearest neibourgh for now
        '''
        if ligne > self.matrix[0][0] or 0 > ligne:  # invalid start point
            raise IndexError
        self.computed_path = [self.matrix[0][ligne], ]
        self.matrix[0][ligne].visite = True  # first point is visited

        tmp = -1
        for _ in xrange(1, self.matrix[0][0]):
            minimum = float('inf')
            for j in xrange(1, self.matrix[0][0] + 1):
                # travel trough the list of point,
                # and search the nearest one
                if 0 < self.matrix[ligne][j] < minimum and\
                    self.matrix[0][j].visite is False:
                    # if the point is near than everything founded
                    # for now, and that it's not marked as visited
                    #mark it as the nearest
                    minimum = self.matrix[ligne][j]
                    tmp = j
            if minimum != float('inf'):
                # add the point to the path
                self.computed_path.append(self.matrix[0][tmp])
                # mark it as visited
                self.matrix[0][tmp].visite = True
                # add the travelled distance to the total one
                self.computed_len += minimum
                ligne = tmp
        self.computed_len += self.matrix[1][tmp]
        self._reset()

    def _draw_distance(self, i, center):
        '''
            Draw the distance between self.matrix[i]
            and self.matrix[i+1]
        '''
        #get the distance between 2 points
        distance = str(self.matrix[self.user_path[i].name][self.user_path[i + 1].name])
        text = self.font.render(distance, True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = center
        self.display.blit(text, textRect)

    def _draw_finished(self):
        ''''
            Draw what has to be drawn when
            every points have been selected
        '''
        # if all points have been selected
        last = self.matrix[0][0] - 1
        for i in xrange(last):  # draw the computed path
            x, y = self._get_corres_pixel(self.computed_path[i].x,
                    self.computed_path[i].y)
            x1, y1 = self._get_corres_pixel(self.computed_path[i + 1].x,
                    self.computed_path[i + 1].y)
            pygame.draw.line(self.display, theme.correction_color,
                    (x + self.hack_x, y + self.hack_y),
                    (x1 + self.hack_x, y1 + self.hack_y))

        #raccord the user's path first point to the last one
        x, y = self._get_corres_pixel(self.computed_path[0].x,
                self.computed_path[0].y)
        x1, y1 = self._get_corres_pixel(self.user_path[last].x,
                self.user_path[last].y)
        pygame.draw.line(self.display, theme.road_color,
                (x + self.hack_x, y + self.hack_y),
                (x1 + self.hack_x, y1 + self.hack_y), 5)

        center = (x + x1) / 2, (y + y1) / 2
        self._draw_distance(0, center)

        # raccord first compted'spath selected point to the last one
        x1, y1 = self._get_corres_pixel(self.computed_path[last].x,
                self.computed_path[last].y)
        pygame.draw.line(self.display, theme.correction_color,
                (x + self.hack_x, y + self.hack_y),
                (x1 + self.hack_x, y1 + self.hack_y))

    def _draw(self):
        '''
            Drawing method
        '''
        if len(self.user_path) > 0:
            # if the user has selected more than 1 point
            for i in xrange(len(self.user_path) - 1):  # draw user's path
                x, y = self._get_corres_pixel(self.user_path[i].x,
                        self.user_path[i].y)
                x1, y1 = self._get_corres_pixel(self.user_path[i + 1].x,
                        self.user_path[i + 1].y)
                pygame.draw.line(self.display, theme.road_color,
                        (x + self.hack_x, y + self.hack_y),
                        (x1 + self.hack_x, y1 + self.hack_y), 5)

                #get the distance between 2 points
                center = (x + x1) / 2, (y + y1) / 2
                self._draw_distance(i, center)

            if self.nbselected == self.matrix[0][0]:
                self._draw_finished()

        for point in self.matrix[0][1:]:  # draw points
            pix = pygame.image.load(random.choice(theme.cities))
            self.display.blit(pix, self._get_corres_pixel(point.x, point.y))

        #user's length
        text = self.font.render('User: ' +
                str(self.user_len), True, (255, 0, 0))
        self.display.blit(text, (10, 10))

        #computed lenght
        text = self.font.render('Computed: ' +
                str(self.computed_len), True, theme.correction_color)
        self.display.blit(text, (10, 20))

    def _update(self, (x, y), button):
        '''
            Update internal data
        '''
        if button != 1 and len(self.user_path) != self.matrix[0][0]\
                and len(self.user_path) > 1:  # cancel the last action on right-clic
            p1 = self.user_path[-1].name
            p2 = self.user_path[-2].name
            self.user_len -= self.matrix[p1][p2]
            self.matrix[0][p1].visite = False
            self.user_path.pop()
            self.nbselected -= 1
            return

        # detection of a click inside a point
        index = 0
        for cpt, point in enumerate(self.matrix[0][1:]):
            real_x, real_y = self._get_corres_pixel(point.x, point.y)
            if real_x < x < self.hack_x + real_x + 10 and\
                    real_y < y < real_y + self.hack_y + 10:
                index = cpt + 1
                break

        if index:  # if the click is on a point
            if self.selected is None:  # if click is on first point
                self.first_som = index
                self.nbselected += 1
                self.matrix[0][index].visite = True
                self.selected = self.matrix[0][index]
                # compute optimal solution
                self._solve(self.matrix[0][index].name)
                self.user_path.append(self.matrix[0][index])
            elif self.matrix[0][index].visite is False:
                # click on a non visited point
                self.user_len += self.matrix[index][self.selected.name]
                self.user_path.append(self.matrix[0][index])
                self.nbselected += 1
                self.matrix[0][index].visite = True
                self.selected = self.matrix[0][index]
            if len(self.user_path) == self.matrix[0][0]:
                # if every points have been selected
                # add the distance between first and last point
                self.user_len += self.matrix[index][self.first_som]
