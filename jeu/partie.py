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
    def __init__(self, application, canvas, balle, raquette, brique, score):
        self.application = application
        self.canvas = canvas
        self.balle = balle
        self.raquette = raquette
        self.brique = brique
        self.score = score

        self.vies = 3
        self.application.afficher_vies(self.vies)

        
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

    def perdre_une_vie(self):
        print("Vie perdue !")
        print(f"Vies restantes : {self.vies}")
        self.vies -= 1
        print(f"Vies restantes après perte : {self.vies}")
        self.application.afficher_vies(self.vies)

        self.balle.x = 400
        self.balle.y = 300
        self.balle.vitesse_x = 5
        self.balle.vitesse_y = 5
        self.canvas.coords(self.balle.id, self.balle.x - self.balle.rayon, self.balle.y - self.balle.rayon, self.balle.x + self.balle.rayon, self.balle.y + self.balle.rayon)

    def boucle_jeu(self):
        # print("Boucle de jeu en cours...")
        self.balle.deplacer()

        if self.balle.est_tombee():
            # print("La balle est tombée ! Vie perdue.")
            self.perdre_une_vie()

            if self.vies <= 0:
                print("Partie terminée !")
                return

        else:
            self.verifier_collisions()

        self.application.fenetre.after(20, lambda: self.boucle_jeu())