# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Définir la balle (position, vitesse, rayon), gérer physique rebonds,
    réinitialisation après vie perdue.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Vitesse progressive, balle traversante, multi-balles, trainée visuelle.
"""


class Balle:
    """
    Balle du jeu.
    Attributs :
        x, y : centre de la balle (pixels).
        rayon : rayon (pixels).
        vitesse_x, vitesse_y : déplacement à chaque pas (pixels).
        canvas : zone de jeu.
        id : identifiant Tkinter du cercle.
    """

    def __init__(self, canvas, x, y, rayon, vitesse_x, vitesse_y):
        """
        But : créer la balle et la dessiner.
        Entrées :
            canvas (tk.Canvas) : zone de jeu.
            x, y (float) : position de départ du centre.
            rayon (int) : rayon de la balle.
            vitesse_x, vitesse_y (float) : vitesse de départ.
        Sortie : aucune.
        """
        self.x = x
        self.y = y
        self.rayon = rayon
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y
        self.canvas = canvas

        self.id = canvas.create_oval(self.x - self.rayon,
                                     self.y - self.rayon,
                                     self.x + self.rayon,
                                     self.y + self.rayon, fill="white")

    def est_tombee(self):
        """
        But : savoir si la balle est sortie par le bas.
        Entrée : aucune.
        Sortie : (bool) True si la balle est tombée.
        """
        return self.y - self.rayon >= self.canvas.winfo_height()

    def deplacer(self):
        """
        But : avancer la balle d'un pas et la faire rebondir sur les murs
        gauche, droit et haut.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.canvas.move(self.id, self.vitesse_x, self.vitesse_y)

        if self.x + self.rayon >= self.canvas.winfo_width():
            self.vitesse_x = -self.vitesse_x
        if self.x - self.rayon <= 0:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.rayon <= 0:
            self.vitesse_y = -self.vitesse_y
