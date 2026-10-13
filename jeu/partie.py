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

        x1,y1,x2,y2 = coords_balle
        rx1,ry1,rx2,ry2 = coords_raquette

        if x1 <= rx2 and x2 >= rx1 and y2 >= ry1 and y1 <= ry2:
            self.balle.vitesse_y = -self.balle.vitesse_y
            print("Collision détectée !")


        self.fenetre.after(20, lambda: self.lecture_coords())

    def point_le_plus_proche(x, y, boite):
        """
        Fonction permettant de trouver le point du rectangle le plus proche d'un point donné
        """
        x_min, y_min, x_max, y_max = boite
        x_proche = min(max(x, x_min), x_max)
        y_proche = min(max(y, y_min), y_max)
        return x_proche, y_proche

    def collision_balle_brique(self, brique):
        """
        Fonction permettant de détecter la collision entre la balle et une brique
        """
        coords_balle = self.canvas.coords(self.balle.id)
        x_balle, y_balle = (coords_balle[0] + coords_balle[2]) / 2, (coords_balle[1] + coords_balle[3]) / 2
        boite_brique = self.canvas.coords(brique.id_canvas)

        x_proche, y_proche = self.point_le_plus_proche(x_balle, y_balle, boite_brique)

        distance = ((x_proche - x_balle) ** 2 + (y_proche - y_balle) ** 2) ** 0.5

        if distance <= self.balle.rayon:
            self.balle.vitesse_y = -self.balle.vitesse_y
            return True
        return False

    def rebond_brique(self, brique):
         x_min, y_min, x_max, y_max = boite
    x_proche, y_proche = point_le_plus_proche(balle.x, balle.y, boite)
    ecart_x = abs(balle.x - x_proche)
    ecart_y = abs(balle.y - y_proche)
    if ecart_x == 0 and ecart_y == 0:
        # Centre à l'intérieur : on choisit l'axe de plus faible pénétration.
        penetration_x = min(balle.x - x_min, x_max - balle.x)
        penetration_y = min(balle.y - y_min, y_max - balle.y)
        face_laterale = penetration_x < penetration_y
    else:
        face_laterale = ecart_x > ecart_y
 
    if face_laterale:
        centre_x = (x_min + x_max) / 2
        if balle.x < centre_x:
            balle.vitesse_x = -abs(balle.vitesse_x)
        else:
            balle.vitesse_x = abs(balle.vitesse_x)
    else:
        centre_y = (y_min + y_max) / 2
        if balle.y < centre_y:
            balle.vitesse_y = -abs(balle.vitesse_y)
        else:
            balle.vitesse_y = abs(balle.vitesse_y)


    def avancer(self):
        self.balle.deplacer()
        self.gerer_collision_briques()

    def est_gagnee(self):
        return len(self.briques) == 0