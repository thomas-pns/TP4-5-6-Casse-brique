# Header
# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Définir la balle (position, vitesse, rayon), gérer physique rebonds, réinitialisation après vie perdue.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Vitesse progressive, balle traversante, multi-balles, trainée visuelle.
"""

class Balle:
    def __init__(self, canvas, x, y, rayon, vitesse_x, vitesse_y):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y
        self.canvas = canvas

        self.id = canvas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon, fill="white")
        

        
        

