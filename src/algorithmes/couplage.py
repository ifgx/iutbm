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

# algorithme
listeFourmis = [("Fourmi A", ""), ("Fourmi B", ""), ("Fourmi C", ""), ("Fourmi D", ""), ("Fourmi E", "")]
listeDesserts = [("Flan", ""), ("Banane", ""), ("Gâteau au chocolat", ""), ("Glace à la fraise", ""), ("Glace à la vanille", "")]

mod = ModelisationCouplage(listeFourmis, listeDesserts, 13)

print "Préferences :"
mod.afficher(mod.preferences)

mod.resoudre()

print "\n\nSolution :"
mod.afficher(mod.solution)


