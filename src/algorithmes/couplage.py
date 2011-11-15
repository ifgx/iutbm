#-*-coding:utf8-*-
from random import choice, randrange

import pygame

class Couplage:
    def __init__(self, display):
        self.display = display
        
        # Génération aléatoire des fourmis et des desserts
        nbFourmis = randrange(3, 6)
        nbDesserts = randrange(3, 6)
        
        theDir = "algorithmes/couplage-data/"
        
        allFourmis = [ ("Fourmi rouge", "fourmi-rouge.png"), ("Fourmi verte", "fourmi-verte.png"), ("Fourmi bleue", "fourmi-bleue.png"), ("Fourmi jaune", "fourmi-jaune.png"), ("Fourmi orange", "fourmi-orange.png") ]
        
        self.imgFourmis = [pygame.image.load(theDir + img).convert_alpha() for _, img in allFourmis]
        
        allDesserts = [ ("Mars", "mars.png"), ("Pomme", "pomme.png"), ("Flan", "flan.png"), ("Twix", "twix.png"), ("Cerise", "cerise.png") ]
        
        self.imgDesserts = [pygame.image.load(theDir + img).convert_alpha() for _, img in allDesserts]
        
        self.fourmis = [allFourmis[i] for i in range(nbFourmis)]
        self.desserts = [allDesserts[i] for i in range(nbDesserts)]
    
    def _draw(self):
        #titre = self.font.render("Bienvenue au Couplage", True, (0,255, 0) )
        #titreRect = titre.get_rect()
        #titreRect.top = 50
        #titreRect.left = 50
        #self.display.blit(text,textRect)
        
        for i, fourmi in enumerate(self.fourmis): 
            self.display.blit(self.imgFourmis[i], (50, 150 * i))
        
        for i, dessert in enumerate(self.desserts):
            self.display.blit(self.imgDesserts[i], (500, 150 * i))

        if False:
            [self.display.blit(i.image, i.rect) for i in self.LSommet]# then we draw the picture of the town

            [pygame.draw.rect(self.display, (255, 0, 255), i.rect,2) for i in self.selected]# then we draw the weight of the link

            pygame.draw.rect(self.display,(255,0,0),self.start.rect,2)
            pygame.draw.rect(self.display,(0,255,0),self.end.rect,2)

            if self.state_game == 1: 
                if (self.weight > self.end.score):
                    text = self.font.render("You did not found the optimal path",True , (0,255,0))
                else:
                    text = self.font.render("Congratulation : you found the optimal path wiht the lenght " + str(self.end.score).replace('[',' '),True , (0,255,0))
                textRect = text.get_rect()
                textRect.center =(self.center_x, 10)
                self.display.blit(text,textRect)

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

    def __init__(self, listeFourmis, listeDesserts, nbCouples):
        # Génération d'une liste de préférences pour les fourmis
        self.preferences = []
        
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


