# Header
# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Orchestrer la boucle de jeu, détecter collisions (balle/raquette, balle/briques, balle/murs), gérer fin de partie (victoire/défaite).

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Power-ups, niveaux multiples, système de combo, sauvegarde/reprise partie.
"""

class Partie:
    def __init__(self, fenetre, canvas, balle, raquette):
        self.fenetre = fenetre
        self.canvas = canvas
        self.balle = balle
        self.raquette = raquette


    def lecture_coords(self):
        coords_balle = self.canvas.coords(self.balle.id)
        coords_raquette = self.canvas.coords(self.raquette.id)
        # print(coords_raquette, coords_balle)

        x1,y1,x2,y2 = coords_balle
        rx1,ry1,rx2,ry2 = coords_raquette

        if x1 <= rx2 and x2 >= rx1 and y2 >= ry1 and y1 <= ry2:
            self.balle.vitesse_y = -self.balle.vitesse_y
            print("Collision détectée !")


        self.fenetre.after(20, lambda: self.lecture_coords())