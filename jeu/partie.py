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
    def __init__(self, fenetre, canvas, balle, raquette, brique, score):
        self.fenetre = fenetre
        self.canvas = canvas
        self.balle = balle
        self.raquette = raquette
        self.brique = brique
        self.score = score

        
    def lecture_coords(self):
        coords_balle = self.canvas.coords(self.balle.id)
        coords_raquette = self.canvas.coords(self.raquette.id)
        # print(coords_raquette, coords_balle)

        return coords_balle, coords_raquette


    def verifier_collisions(self):
        coords_balle, coords_raquette = self.lecture_coords()
        x1,y1,x2,y2 = coords_balle
        rx1,ry1,rx2,ry2 = coords_raquette

        if x1 <= rx2 and x2 >= rx1 and y2 >= ry1 and y1 <= ry2:
            self.balle.vitesse_y = -self.balle.vitesse_y
            print("Collision détectée !")
    
    def boucle_jeu(self):
        self.balle.deplacer()

        if self.balle.est_tombee():
            pass
            # self.perdre_une_vie()
        else:
            self.verifier_collisions()

        self.fenetre.after(20, lambda: self.lecture_coords())