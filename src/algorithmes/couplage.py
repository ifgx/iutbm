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
            if premier:
                if elemt[0] == element:
                    return True
            else:
                if elemt[1] == element:
                    return True
        return False

    def __init__(self, listeFourmis, listeDesserts, nbCouples):
        # Génération d'une liste de préférences pour les fourmis
        self.preferences = []
        
        self.fourmis = listeFourmis
        self.desserts = listeDesserts
        
        assert nbCouples <= (len(listeFourmis) * len(listeDesserts))
        
        for i in range(nbCouples):
            is_init = True
            while(is_init or self.preferences.count((fourmi, dessert)) > 0):
                is_init = False
                fourmi = choice(listeFourmis)
                dessert = choice(listeDesserts)

            self.preferences.append((fourmi, dessert))
        
        # On ajoute un couple pour chaque fourmi et chaque dessert qui ne sont pas encore satisfaites/servis
        for fourmi in listeFourmis:
            if not self.element_en_liste(self.preferences, fourmi, True):
                is_init = True
                while(is_init or self.preferences.count((fourmi, dessert)) > 0):
                    is_init = False
                    dessert = choice(listeDesserts)

                self.preferences.append((fourmi, dessert))

        for dessert in listeDesserts:
            if not self.element_en_liste(self.preferences, dessert, False):
                is_init = True
                while(is_init or self.preferences.count((fourmi, dessert)) > 0):
                    is_init = False
                    fourmi = choice(listeFourmis)

                self.preferences.append((fourmi, dessert))

    """
        Retourne les fourmis qui n'apparaissent qu'une fois dans
         le tableau des préférences.
    """
    def fourmi_une_fois(self):
        # Nombre d'occurrences de chaque fourmi
        nb_occurrences = []
        for f in self.fourmis:
            nb_occurrences.append(0)
        
        for p in self.preferences:
            nb_occurrences[self.fourmis.index(p[0])] += 1
        
        fourmis_1 = []
        for i in range(len(nb_occurrences)):
            if nb_occurrences[i] == 1:
                fourmis_1.append(self.fourmis[i])
        
        return fourmis_1
        

    def resoudre(self):
        print self.preferences
        for fourmi in self.fourmi_une_fois():
            print "La fourmi", fourmi[0], "n'apparait qu'une fois"

# algorithme
listeFourmis = [("Fourmi A", "fourmi-a.png"), ("Fourmi B", "fourmi-b.png"), ("Fourmi C", "fourmi-c.png")]
listeDesserts = [("Flan", "flan.png"), ("Banane", "banane.png"), ("Gâteau au chocolat", "gateau.png")]

mod = ModelisationCouplage(listeFourmis, listeDesserts, 50)

mod.resoudre()


