#!/bin/env python
# -*- coding: utf-8 -*-
import random


class Graphe(object):
    """
        La classe Graphe permet de générer un graphe connexe avec nbSommet
    """
    def __init__(self,nbSommet,Min,Max):
        self.Matrix = [[ float('inf') for i in range(nbSommet)] for i in range(nbSommet)]
        self.nbSommet=nbSommet
        for i in range(nbSommet-1): 
            poids=random.randint(Min,Max)
            self.Matrix[i+1][i] = poids
        for i in range(nbSommet):
            for j in range(i):
                chance= random.random() *100
                if chance < 10:
                    poids=random.randint(Min,Max)
                    self.Matrix[i][j] = poids
        for i in range(nbSommet):
            self.Matrix[i][i] = float('inf')
            for j in range(i):
                self.Matrix[j][i] = self.Matrix[i][j]
        self.LSommet = [Sommet(i) for i in range(nbSommet)]
        self.debut=random.choice(self.LSommet).indice
        self.LSommet[self.debut].score = 0
        self.fin = (random.randint(1,nbSommet-1)+self.debut) % nbSommet
        

    def resoudre(self):
        PasencoreVu = self.LSommet[:]
        while PasencoreVu:
            sommet1 = min(PasencoreVu, key = visiterS) 
            sommet1.visiter = True
            PasencoreVu.remove(sommet1)
            self.mettre_a_jour(sommet1)
        print("resultat : \n")
        print(self.LSommet[self.fin].score)
        chemin=self.LSommet[self.fin].precedent
        while chemin != None:
            print chemin.indice
            chemin=chemin.precedent            
        

    def mettre_a_jour(self,sommet1):
        for i in range(self.nbSommet):
            if self.LSommet[i].score > sommet1.score + self.Matrix[sommet1.indice][i]:
                self.LSommet[i].score = sommet1.score + self.Matrix[sommet1.indice][i]
                self.LSommet[i].precedent=sommet1

    def affiche(self):
        print('Sommet de début')
        print(self.debut)
        print('Sommet de fin')
        print(self.fin)
        for i in self.Matrix:
            print i


    def PasencoreVu(self):
        for i in self.LSommet:
            if i.visiter == False:
                return True
        return False

'''
    La classe Sommet permet de définir des sommets avec un indice, un score initialisé à 0, un boolean visiterr et une variable precedent qui contiendra la valeur du sommet précedent
'''
class Sommet(object):
    def __init__(self,indice):
        self.indice = indice
        self.score = float('inf')
        self.visiter = False
        self.precedent = None

def visiterS(x):
    if x.visiter == False:
        return x.score
    else:
        return float('inf')
