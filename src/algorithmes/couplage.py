#-*-coding:utf8-*-
from random import choice, randrange, shuffle

import pygame
import algo

class Couplage(algo.Algo):
    def __init__(self, display):
        algo.Algo.__init__(self, display)
        self.text = 'Coupling problem'
        self.description = 'Given a list of customers and a list of pizzas,#\
you have to link both entities so as to satisfy them all, taking into#\
account that each pizza can only be given once.#\
A client is satisfied when he has been given one pizza.'

        
        # Génération aléatoire des fourmis et des desserts
        nbFourmis = randrange(3, 6)
        nbDesserts = randrange(3, 6)
        
        # print "Sélection de", nbFourmis, "fourmis et", nbDesserts, "desserts."
        
        theDir = "ui/pix/couplage/"
        
        allFourmis = [
            ("George",  "client-blanc.png" ),
            ("Ulrich",  "client-bleu.png"  ),
            ("Michael", "client-orange.png"),
            ("John",    "client-vert.png"  ),
            ("Patrick", "client-violet.png")]
        
        allDesserts = [
            ("Caper pizza",       "pizza-capres.png"    ),
            ("Margherita pizza",  "pizza-margherita.png"),
            ("Onions pizza",      "pizza-oignons.png"   ),
            ("Pepperoni pizza",   "pizza-pepperoni.png" ),
            ("Mushroom pizza",    "pizza-reine.png"     )]
        
        shuffle(allFourmis)
        shuffle(allDesserts)
        
        self.imgFourmis = [pygame.image.load(theDir + img).convert_alpha() for _, img in allFourmis]
        self.imgDesserts = [pygame.image.load(theDir + img).convert_alpha() for _, img in allDesserts]
        
        self.fourmis = [allFourmis[i] for i in range(nbFourmis)]
        self.desserts = [allDesserts[i] for i in range(nbDesserts)]
        
        self.fourmiSelectionnee = (-1, None)
        # handles the selection of a dessert in the preferences list, to highlight it on the right
        self.dessertSelectionne = None
        
        self.erreur = ""
        
        self.model = ModelisationCouplage(self.fourmis, self.desserts, 5)
        self.model.resoudre()
        
        self.marge_prefs = 20
        self.marge_gauche = 35
        self.marge_droite = 35
        self.marge_haut = 30
        
        self.largeur_icone = self.imgFourmis[0].get_rect().width * self.maxx / self.display.get_rect().width 
        self.hauteur_icone = self.imgFourmis[0].get_rect().height * self.maxy / self.display.get_rect().height
        
        self.pas_vertical = 2 + self.hauteur_icone
        self.pas_horizontal = 2 + self.largeur_icone
        
        self.rectFourmis = []
        self.rectDesserts = []
        self.rectPrefs = []
    
    def _update(self, (x, y), button):
        # reset error
        self.erreur = ""
        
        if button == 1:
            bgClick = True
            
            # Check if a fourmi is selected
            for i, fourmi in self.rectFourmis:
                if fourmi.collidepoint(x, y):
                    self.fourmiSelectionnee = (i, self.fourmis[i])
                    bgClick = False
            
            # Check if a dessert is selected
            for i, rect in self.rectDesserts:
                if rect.collidepoint(x, y):
                    # a dessert is clicked
                    dessert = self.desserts[i]
                    if self.fourmiSelectionnee != (-1, None):
                        fourmi = self.fourmiSelectionnee[1]
                        dessertSelectionne = True
                        # print "Cliqué sur le dessert", i, "(", dessert[0], ")"
                        # check if the fourmi or dessert is not already involved
                        if not self.model.fourmi_dans(fourmi, self.model.proposition):
                            if not self.model.dessert_dans(dessert, self.model.proposition):
                                if dessert in self.model.desserts_de_fourmi(fourmi):
                                    # print "Validé la combinaison (", fourmi[0], ",", dessert[0], ")"
                                    self.model.proposition.append((fourmi, dessert))
                                else:
                                    self.erreur = fourmi[0] + " does not like this pizza"
                            else:
                                # print "Le dessert", dessert[0], "est déjà attribué"
                                self.erreur = "The pizza " + dessert[0] + " is already assigned"
                        else:
                            # print "La fourmi", fourmi[0], "est déjà attribuée"
                            self.erreur = "The customer " + fourmi[0] + " has already a pizza"
                    else:
                        self.erreur = "Please select a customer first."
                    bgClick = False
            
            # Check if a preference is selected (if so, highlight the corresponding dessert)
            for dessert, rect in self.rectPrefs:
                if rect.collidepoint(x, y):
                    self.dessertSelectionne = dessert
                    bgClick = False
            
            if bgClick:
                self.fourmiSelectionnee = (-1, None)
                self.dessertSelectionne = None
        elif button == 3:
            if len(self.model.proposition) != 0:
                self.model.proposition.pop()
        
    
    def _draw(self):
        self.rectFourmis = []
        self.rectDesserts = []
        self.rectPrefs = []
        
        titre = self.font.render("Help the pizza deliveryman to deliver pizzas to his customers", True, (0, 255, 0) )
        titreRect = titre.get_rect()
        titreRect.top = 48
        titreRect.centerx = self.display.get_rect().width / 2
        self.display.blit(titre, titreRect)
        
        desc = self.font.render("Click on a customer to select it. Then, click on the pizza you have chosen for this customer.", True, (255, 255, 255) )
        descRect = desc.get_rect()
        descRect.top = 64
        descRect.centerx = self.display.get_rect().width / 2
        self.display.blit(desc, descRect)
        
        if self.erreur != "":
            err = self.font.render(self.erreur, True, (255, 0, 0) )
            errRect = err.get_rect()
            errRect.top = 96
            errRect.centerx = self.display.get_rect().width / 2
            self.display.blit(err, errRect)

        if len(self.model.proposition) == self.model.max_flow: 
            congrats = self.font.render("Congratulations! You have found one of the possible solutions.", True, (0, 255, 0) )
            congratsRect = congrats.get_rect()
            congratsRect.top = 128
            congratsRect.centerx = self.display.get_rect().width / 2
            self.display.blit(congrats, congratsRect)
        
        
        for couple in self.model.proposition:
            fourmiI = self.fourmis.index(couple[0])
            dessertI = self.desserts.index(couple[1])
            pygame.draw.line(self.display, (255, 0, 0),
                self._get_corres_pixel(self.marge_gauche             + (self.largeur_icone / 2), self.marge_haut + (self.pas_vertical * fourmiI)  + (self.hauteur_icone / 2)),
                self._get_corres_pixel(self.maxx - self.marge_droite + (self.largeur_icone / 2), self.marge_haut + (self.pas_vertical * dessertI) + (self.hauteur_icone / 2)),
                3)
        
        if self.show_solution:
            for couple in self.model.solution:
                fourmiI = self.fourmis.index(couple[0])
                dessertI = self.desserts.index(couple[1])
                pygame.draw.line(self.display, (0, 128, 0),
                    self._get_corres_pixel(self.marge_gauche             + (self.largeur_icone / 2), self.marge_haut + (self.pas_vertical * fourmiI)  + (self.hauteur_icone / 2)),
                    self._get_corres_pixel(self.maxx - self.marge_droite + (self.largeur_icone / 2), self.marge_haut + (self.pas_vertical * dessertI) + (self.hauteur_icone / 2)),
                    3)
        
        pref = self.font.render("Preferences for each customer:", True, (255, 255, 255))
        prefRect = pref.get_rect()
        prefRect.right, prefRect.bottom = self._get_corres_pixel(self.marge_prefs + self.pas_horizontal, self.marge_haut - 2)
        self.display.blit(pref, prefRect)
        
        for i, fourmi in enumerate(self.fourmis):
            if (i, fourmi) == self.fourmiSelectionnee:
                couleur = (0, 255, 0)
            else:
                couleur = (255, 255, 255)
            
            nom = self.font.render(fourmi[0], True, couleur)
            x, y = self._get_corres_pixel(self.marge_gauche - 2, self.marge_haut + (i * self.pas_vertical) + (self.hauteur_icone / 2))
            nomRect = nom.get_rect()
            nomRect.right = x
            nomRect.centery = y
            self.display.blit(nom, nomRect)
            self.rectFourmis.append((i, self.display.blit(self.imgFourmis[i], self._get_corres_pixel(self.marge_gauche, self.marge_haut + (self.pas_vertical * i)))))
            
            # draw the preferences of the fourmi
            for j, pref in enumerate(self.model.desserts_correspondants(fourmi)):
                self.rectPrefs.append((pref, self.display.blit(
                    self.imgDesserts[self.desserts.index(pref)],
                    self._get_corres_pixel(self.marge_prefs - (j * self.pas_horizontal), self.marge_haut + (self.pas_vertical * i))
                )))
        
        for i, dessert in enumerate(self.desserts):
            if dessert == self.dessertSelectionne:
                couleur = (0, 255, 0)
            else:
                couleur = (255, 255, 255)
        
            nom = self.font.render(dessert[0], True, couleur)
            x, y = self._get_corres_pixel(self.maxx - self.marge_droite + self.largeur_icone + 2, self.marge_haut + (i * self.pas_vertical) + (self.hauteur_icone / 2))
            nomRect = nom.get_rect()
            nomRect.left = x
            nomRect.centery = y
            self.display.blit(nom, nomRect)
            self.rectDesserts.append((i, self.display.blit(self.imgDesserts[i], self._get_corres_pixel(self.maxx - self.marge_droite, self.marge_haut + (self.pas_vertical * i)))))
        
        
class Edge(object):
    def __init__(self, u, v, w,chemin = False):
        self.source = u
        self.sink = v
        self.capacity = w
        self.passage = 0
        self.chemin = chemin


    def __repr__(self):
        return "%s->%s:%s %s" % (self.source, self.sink, self.capacity,self.passage)

class ModelisationCouplage:
    """
        Vérifie si l'élément `element' fait partie de la liste `liste'
        `liste' est une liste de tuples (a, b). `premier' définit si l'on doit tester
        si l'élément est à place de a ou b.
    """
    def element_en_liste(self, liste, element, premier):
        for elemt in liste:
            if elemt[1 - premier] == element:
                return True
        return False
    
    def fourmi_dans(self, fourmi, liste):
        """
            Vérifie si une fourmi est déjà présente dans la liste fournie
        """
        return self.element_en_liste(liste, fourmi, 1)
    
    def dessert_dans(self, dessert, liste):
        """
            Vérifie si une fourmi est déjà présente dans la liste fournie
        """
        return self.element_en_liste(liste, dessert, 0)

    def add_vertex(self, vertex):
        self.adj[vertex] = []
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u, v, w=0,chemin = False):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w,chemin)
        redge = Edge(v,u,0,chemin)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def find_path(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge,residual) in path:
                result = self.find_path( edge.sink, sink, path + [(edge,residual)] ) 
                if result != None:
                    return result



    def __init__(self, listeFourmis, listeDesserts, nbCouples):
        # Génération d'une liste de préférences pour les fourmis
        self.preferences = []
        self.solution = []
        self.proposition = []

        self.adj = {}
        self.flow = {}
        
        self.fourmis = listeFourmis
        self.desserts = listeDesserts
        
        assert nbCouples <= (len(listeFourmis) * len(listeDesserts))
        
        self.add_vertex('S')
        self.add_vertex('T')

        for i in self.fourmis:
            self.add_vertex(i)
            self.add_edge('S',i,1)

        for i in self.desserts:
            self.add_vertex(i)
            self.add_edge(i,'T',1)

        for i in xrange(nbCouples):
            fourmi = choice(listeFourmis)
            dessert = choice(listeDesserts)
            while self.preferences.count((fourmi, dessert)):
                fourmi = choice(listeFourmis)
                dessert = choice(listeDesserts)
            self.preferences.append((fourmi, dessert))
            self.add_edge(fourmi,dessert,100,True)
        
        # On ajoute un couple pour chaque fourmi et chaque dessert qui ne sont pas encore satisfaites/servis
        for fourmi in listeFourmis:
            if not self.element_en_liste(self.preferences, fourmi, 1):
                dessert = choice(listeDesserts)
                while self.preferences.count((fourmi, dessert)):
                    dessert = choice(listeDesserts)
                self.preferences.append((fourmi, dessert))
                self.add_edge(fourmi,dessert,100,True)
        
        for dessert in listeDesserts:
            if not self.element_en_liste(self.preferences, dessert, 0):
                fourmi = choice(listeFourmis)
                while self.preferences.count((fourmi, dessert)):
                    fourmi = choice(listeFourmis)
                self.preferences.append((fourmi, dessert))
                self.add_edge(fourmi,dessert,100,True)
    
    def desserts_correspondants(self, fourmi):
        """
            Retourne la liste des desserts correspondants à une fourmi donnée.
        """
        return [p[1] for p in self.preferences if p[0] == fourmi]
    
    
    def desserts_de_fourmi(self, fourmi):
        """
            Retourne la liste des desserts non encore attribués, correspondant
             à une fourmi donnée.
        """
        return [d for f, d in self.preferences if f == fourmi]
    
    def afficher(self, liste):
        for fourmi, dessert in liste:
            print fourmi[0], "=>", dessert[0]
    
    def resoudre(self):
        source = 'S'
        sink = 'T'
        self.solution = []


        path = self.find_path(source, sink, [])
        while path != None:
            flow = min(res for edge,res in path)
            for edge,res in path:
                self.flow[edge] += flow
                edge.passage += flow
                self.flow[edge.redge] -= flow
                edge.redge.passage -= flow
            path = self.find_path(source, sink, [])

        for i in self.flow:
            if i.passage  == 1 and i.chemin==True:
                self.solution.append((i.source,i.sink))

        self.max_flow = sum(self.flow[edge] for edge in self.get_edges(source))
