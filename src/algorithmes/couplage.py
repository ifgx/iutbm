#-*-coding:utf8-*-
from random import choice, randrange, shuffle

import pygame
import algo

class Couplage(algo.Algo):
    def __init__(self, display):
        algo.Algo.__init__(self, display)
        
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
        
        self.erreur = ""
        
        self.model = ModelisationCouplage(self.fourmis, self.desserts, 5)
        self.model.resoudre()
    
    def _update(self, (x, y),button):
        # reset error
        self.erreur = ""
        
        if button == 1:
            # if we have selected a fourmi, then create a line from the fourmi to the dessert
            dessertSelectionne = False
            for i, dessert in enumerate(self.desserts):
                # check whether the user clicked on the dessert
                if x >= 128 + 384 and x <= 128 + 384 + 32: # x coordinate is good
                    y_coord = 192 + (64 * i)
                    if y >= y_coord and y <= y_coord + 32: # y coordinate is good
                        # a dessert is clicked
                        if self.fourmiSelectionnee != (-1, None):
                            fourmi = self.fourmiSelectionnee[1]
                            dessertSelectionne = True
                            # print "Cliqué sur le dessert", i, "(", dessert[0], ")"
                            # check if the fourmi or dessert is not already involved
                            if not self.model.fourmi_dans(fourmi, self.model.proposition):
                                if not self.model.dessert_dans(dessert, self.model.proposition):
                                    # print "Validé la combinaison (", fourmi[0], ",", dessert[0], ")"
                                    self.model.proposition.append((fourmi, dessert))
                                else:
                                    # print "Le dessert", dessert[0], "est déjà attribué"
                                    self.erreur = "The pizza " + dessert[0] + " is already assigned"
                            else:
                                # print "La fourmi", fourmi[0], "est déjà attribuée"
                                self.erreur = "The customer " + fourmi[0] + " has already a pizza"
                            
                        else:
                            self.erreur = "Please select a customer first."
            if not dessertSelectionne:
                # deselect the fourmi
                self.fourmiSelectionnee = (-1, None)
            
            for i, fourmi in enumerate(self.fourmis):
                # check whether the user clicked on the fourmi
                if x >= 128 and x <= 128 + 32: # x coordinate is good
                    y_coord = 192 + (64 * i)
                    if y >= y_coord and y <= y_coord + 32: # y coordinate is good
                        # print "Cliqué sur la fourmi", i, "(", fourmi[0], ")"
                        self.fourmiSelectionnee = (i, fourmi)
        elif button == 3:
            if len(self.model.proposition) != 0:
                self.model.proposition.pop()
        
    
    def _draw(self):
        titre = self.font.render("Help the pizza deliveryman to deliver pizzas to his customers", True, (0, 255, 0) )
        titreRect = titre.get_rect()
        titreRect.top = 48
        titreRect.centerx = self.display.get_rect().width / 2
        self.display.blit(titre, titreRect)
        
        desc = self.font.render("Click on a customer to see which pizza they like. Then, click on the pizza you have chosen for this customer.", True, (255, 255, 255) )
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
        
        for couple in self.model.proposition:
            fourmiI = self.fourmis.index(couple[0])
            dessertI = self.desserts.index(couple[1])
            pygame.draw.line(self.display, (255, 0, 0), (128 + 16, 192 + (64 * fourmiI) + 16), (128 + 384 + 16, 192 + (64 * dessertI) + 16), 3)
        
        if len(self.model.proposition) == len(self.model.solution):
            for couple in self.model.solution:
                fourmiI = self.fourmis.index(couple[0])
                dessertI = self.desserts.index(couple[1])
                pygame.draw.line(self.display, (0, 255, 255), (128 + 16, 192 + (64 * fourmiI) + 16), (128 + 384 + 16, 192 + (64 * dessertI) + 16), 3)

        for i, fourmi in enumerate(self.fourmis):
            nom = self.font.render(fourmi[0], True, (255, 255, 255))
            nomRect = nom.get_rect()
            nomRect.centery = 192 + (64 * i) + 18
            nomRect.right = 128 - 8
            self.display.blit(nom, nomRect)
            self.display.blit(self.imgFourmis[i], (128, 192 + (64 * i)))
        
        for i, dessert in enumerate(self.desserts):
            nom = self.font.render(dessert[0], True, (255, 255, 255))
            nomRect = nom.get_rect()
            nomRect.centery = 192 + (64 * i) + 18
            nomRect.left = 128 + 384 + 32 + 8
            self.display.blit(nom, nomRect)
            self.display.blit(self.imgDesserts[i], (128 + 384, 192 + (64 * i)))
        
        if self.fourmiSelectionnee != (-1, None):
            # draw the preferences of the fourmi at the bottom of the screen
            # fourmi pic
            pic = self.imgFourmis[self.fourmiSelectionnee[0]]
            self.display.blit(pic, (192, self.display.get_rect().height - 64))
            
            # fourmi name
            nom = self.font.render(self.fourmiSelectionnee[1][0] + " likes:", True, (0, 255, 0) )
            nomRect = nom.get_rect()
            nomRect.bottom = self.display.get_rect().height - 40
            nomRect.left = 192 + 32 + 8
            self.display.blit(nom, nomRect)
            
            # fourmi preferences
            for i, pref in enumerate(self.model.desserts_correspondants(self.fourmiSelectionnee[1])):
                self.display.blit(self.imgDesserts[self.desserts.index(pref)], (192 + 32 + 128 + (i * 64), self.display.get_rect().height - 64))

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

    def __init__(self, listeFourmis, listeDesserts, nbCouples):
        # Génération d'une liste de préférences pour les fourmis
        self.preferences = []
        self.solution = []
        self.proposition = []
        
        self.fourmis = listeFourmis
        self.desserts = listeDesserts
        
        assert nbCouples <= (len(listeFourmis) * len(listeDesserts))
        
        for i in xrange(nbCouples):
            fourmi = choice(listeFourmis)
            dessert = choice(listeDesserts)
            while self.preferences.count((fourmi, dessert)):
                fourmi = choice(listeFourmis)
                dessert = choice(listeDesserts)
            self.preferences.append((fourmi, dessert))
        
        # On ajoute un couple pour chaque fourmi et chaque dessert qui ne sont pas encore satisfaites/servis
        for fourmi in listeFourmis:
            if not self.element_en_liste(self.preferences, fourmi, 1):
                dessert = choice(listeDesserts)
                while self.preferences.count((fourmi, dessert)):
                    dessert = choice(listeDesserts)
                self.preferences.append((fourmi, dessert))
        
        for dessert in listeDesserts:
            if not self.element_en_liste(self.preferences, dessert, 0):
                fourmi = choice(listeFourmis)
                while self.preferences.count((fourmi, dessert)):
                    fourmi = choice(listeFourmis)
                self.preferences.append((fourmi, dessert))
    
    def desserts_correspondants(self, fourmi):
        """
            Retourne la liste des desserts correspondants à une fourmi donnée.
        """
        return [p[1] for p in self.preferences if p[0] == fourmi]
    
    def get_nb_occurrences(self):
        """
            Retourne une liste contenant la liste des occurrences
             de chaque fourmi.
        """
        nb_occurrences = [0 for f in self.fourmis]
        
        for p in self.preferences:
            nb_occurrences[self.fourmis.index(p[0])] += 1
        
        return nb_occurrences
    
    def occurrences_de_fourmi(self, nb_fois):
        """
            Retourne une liste des fourmis qui n'apparaissent que nb_fois dans
             le tableau des préférences.
        """ 
        return [self.fourmis[i] for i, j in enumerate(self.get_nb_occurrences()) if j == nb_fois]
    
    def desserts_de_fourmi(self, fourmi):
        """
            Retourne la liste des desserts non encore attribués, correspondant
             à une fourmi donnée.
        """
        return [d for f, d in self.preferences if f == fourmi]
    
    def supprimer_preferences_de(self, fourmi, dessert):
        """
            Supprime tous les couples contenant la fourmi ou le dessert
             fourni en paramètre.
        """
        
        # print("---- [spd]", len(self.preferences), "couples à traiter (", self.preferences, ")")
        
        i = 0
        while i < len(self.preferences):
            # print("---- [spd] couple", preference)
            if(self.preferences[i][0] == fourmi or self.preferences[i][1] == dessert):
                # print("---- [spd] supprimé")
                self.preferences.pop(i)
            else:
                i += 1
    
    def fourmi_satisfaite(self, fourmi):
        """
            Retourne si la fourmi fournie en paramètre est déjà satisfaite.
        """
        for f, d in self.solution:
            if f == fourmi:
                return True
        return False
    
    def afficher(self, liste):
        for fourmi, dessert in liste:
            print fourmi[0], "=>", dessert[0]
    
    def resoudre(self):
        self.solution = []
        sav_preferences = list(self.preferences)
        
        while len(self.preferences) != 0:
            for i in range(1, 1 + max(self.get_nb_occurrences())):
                # print("- Traitement des fourmis de niveau", i)
                for fourmi in self.occurrences_de_fourmi(i):
                    # print("-- Traitement de la fourmi", fourmi[0])
                    for dessert in self.desserts_de_fourmi(fourmi):
                        # print("--- La", fourmi[0], "aime le", dessert[0])
                        if not self.fourmi_satisfaite(fourmi):
                            # print("--- Succès! Don du dessert", dessert[0], "à la fourmi", fourmi[0])
                            self.solution.append((fourmi, dessert))
                            self.supprimer_preferences_de(fourmi, dessert)
                        else:
                            # print("--- Elle est déjà satisfaite")
                            self.supprimer_preferences_de(fourmi, None)
                # print("- Fin du tour, il reste", len(self.preferences), "couples")
                # print("- Couples restants:", self.preferences, ", couples trouvés:", self.solution)
        
        self.preferences = sav_preferences


if False:
    # algorithme
    listeFourmis = [("Fourmi A", ""), ("Fourmi B", ""), ("Fourmi C", ""), ("Fourmi D", ""), ("Fourmi E", "")]
    listeDesserts = [("Flan", ""), ("Banane", ""), ("Gâteau au chocolat", ""), ("Glace à la fraise", ""), ("Glace à la vanille", "")]

    mod = ModelisationCouplage(listeFourmis, listeDesserts, 13)

    print "Préferences :"
    mod.afficher(mod.preferences)

    mod.resoudre()

    print "\n\nSolution :"
    mod.afficher(mod.solution)


