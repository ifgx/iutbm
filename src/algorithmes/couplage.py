#-*-coding:utf8-*-
from random import choice

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
        for preference in self.preferences:
            if(preference[0] == fourmi or preference[1] == dessert):
                self.preferences.remove(preference)
    
    def resoudre(self):
        solution = []
        
        print self.preferences
        
        for i in range(1, 1 + max(self.get_nb_occurrences())):
            print "- Traitement des fourmis de niveau", i
            for fourmi in self.occurrences_de_fourmi(i):
                print "-- Traitement de la fourmi", fourmi[0]
                for dessert in self.desserts_de_fourmi(fourmi):
                    print "--- La", fourmi[0], "aime le", dessert[0]
                    solution.append((fourmi, dessert))
                    self.supprimer_preferences_de(fourmi, dessert)
        
        print solution

# algorithme
listeFourmis = [("Fourmi A", "fourmi-a.png"), ("Fourmi B", "fourmi-b.png"), ("Fourmi C", "fourmi-c.png")]
listeDesserts = [("Flan", "flan.png"), ("Banane", "banane.png"), ("Gâteau au chocolat", "gateau.png")]

mod = ModelisationCouplage(listeFourmis, listeDesserts, 3)

mod.resoudre()


