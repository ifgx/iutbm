# -*- coding: utf-8 -*-

""" 
    Classe Graph:
    Un graphe est composé de Points et de Liens entre les points
"""    


class Graph(object):

    """
    Constructeur:
        Le constructeur n'a besoin d'aucun argument
        On ajoutera les points et les liens au fur et à mesure
    """
    def __init__(self):
        self.Lpoint=[]
        self.Llien=[]
        self.fin=0
        self.debut=0

    """
    Méthode:
        addPoint(A)
            Permet de créer un Point de nom A qui sera ajouté dans le graphe

        addLien(Np1,Np2,valeur)
            Permet de créer un Lien pondéré de poids=valeur qui relie les points d'indice Np1 et Np2 présent dans la liste des points du graphe 

        Pfin(indice)
            Permet de définir le point d'arrivée 

        Pdebut(indice)
            Permet de définir le point de début

        Dijkstra()
               fonction qui calcule le plus court chemin en utilisant l'algorithme de dijkstra   
    """       

    def addPoint(self,nom):
        self.Lpoint.append(Point(nom))

    def addLien(self,Np1,Np2,valeur):
        if (Np1<len(self.Lpoint) and Np2<len(self.Lpoint)):
            self.Llien.append(Lien(self.Lpoint[Np1],self.Lpoint[Np2],valeur))

    def Pfin(self,indice):
        if indice<len(self.Lpoint):
            self.fin=indice

    def Pdebut(self,indice):
        if indice<len(self.Lpoint):
            self.debut=indice


    def Dijkstra(self):
        self.Lpoint[self.debut].debut()
        PasencoreVu=[]
        for x in self.Lpoint:
            PasencoreVu.append(x)
        while PasencoreVu:
            noeud_1=minimum(PasencoreVu)
            for lien in noeud_1.Lien:
                mettre_jour(noeud_1)

        print self.Lpoint[self.fin].valeur
        self.Lpoint[self.fin].affiche_chemin()

"""
    Classe Point:
        Un point est défini par:
            un nom qui est passer en appel dans le constructeur
            la liste des lien auquel il est reliée
            la valeur est la somme des lien qui permet d'arriver du point de départ jusqu'a ce point (initialement il est a -1 qui ici symbolize l'infini)
            le chemin est une liste qui contient les point par lequuel on doit passer pour arriver a ce point
    
"""
        
class Point(object):

    """
        Constructeur:
            Le constructeur prend le nom du point en argument et il initialize la valeur à -1  
    """
    def __init__(self,name):
        self.name=name #le nom du point
        self.valeur=-1 #la valeur nécessaire pour allez au point, ici -1 sera équivalent à plus infini
        self.Lien=[] #la liste des segement auquel le point est lier
        self.chemin=[] #la liste des point par laquelle on a du passer pour arriver a ce point

    """
        Méthode:
            addChemin(new)
            Cette méthode permet de créer la liste qui contient le chemin pour arriver du point de début a ce point

            debut(L)
            Cette méthode permet de définir le point de début

            affiche_chemin()
            Cette méthode permet d'afficher le chemin du point de début jusqu'au point choisie

            looknext()
            cette méthode permet de trouver le lien le plus court qui est relier a ce point


    """
    def addChemin(self,new):
        self.chemin = [i for i in new.chemin]
        self.chemin.append(new)
    
    def debut(self):
        self.valeur=0 

    def affiche_chemin(self):
        print '\n'.join(i.name for i in self.chemin)

    def looknext(self):#cherche le noeud le plus proche
        minimum = self.Lien[0]
        for i in self.Lien:
            if i.valeur<minimum.valeur and not minimum.visit:
                minimum = i
        return minimum.other(self)


class Lien(object):
    """
        Constructeur:
        Permet de créer un lien pondérer de poids=valeur qui relie les points d'indice Np1 et Np2 
    """
    def __init__(self,A,B,valeur):
        self.A=A
        self.B=B
        self.valeur=valeur
        A.Lien.append(self)
        B.Lien.append(self)
    """
        Méthode:
        other(A)
        Cette méthode permet de trouver le point autre que A qui est reliée par le Lien
    """
    def other(self,A):
        if A==self.A:
            return self.B
        elif A==self.B:
            return self.A
        else :
            print "error"

"""
    minimum(Pt):
        Cette fonction permet de trouver le point contenu dans la liste Pt qui a la plus petit valeur (-1 étant considérer comme plus infini
"""
def minimum(Pt):
    minimum=Pt[0]
    num=0
    for c,i in enumerate(Pt):
	    if i.valeur>=0 and i.valeur<minimum.valeur:
		minimum=i
		num=c
    del Pt[num]
    return minimum

"""
    mettre_jour(point1):
        Cette fonction mets a jour les valeurs des points qui sont relir au point1
        
"""
def mettre_jour(point1):
    for x in point1.Lien:
        point2=x.other(point1)
        if point2.valeur > point1.valeur+x.valeur or point2.valeur==-1:
            point2.valeur= point1.valeur+x.valeur
            point2.addChemin(point1)

    

#création d'un objet graph
graph=Graph()

#initialisation des Points
graph.addPoint("A")
graph.addPoint("B")
graph.addPoint("C")
graph.addPoint("D")
graph.addPoint("E")
graph.addPoint("F")

#initialisation des Liens
graph.addLien(0,1,6)
graph.addLien(0,2,3)
graph.addLien(1,2,2)
graph.addLien(1,3,1)
graph.addLien(3,2,5)
graph.addLien(2,4,7)
graph.addLien(4,3,3)
graph.addLien(4,5,6)
graph.addLien(5,3,4)

#définition du début et de la fin
graph.Pdebut(0)
graph.Pfin(5)

graph.Dijkstra()
