# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Définir la raquette (position, dimensions, vitesse), gérer déplacements
    clavier/souris, limiter aux bords écran.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Raquette qui s'agrandit/rétrécit, effet "collant", visuel particules.
"""


class Raquette():
    """
    Raquette du joueur.
    Attributs :
        canvas : zone de jeu.
        largeur, hauteur : dimensions (pixels).
        vitesse : déplacement à chaque appui sur une flèche (pixels).
        x, y : coin supérieur gauche (pixels).
        id : identifiant Tkinter du rectangle.
    """

    def __init__(self, canvas, largeur=100, hauteur=20, vitesse=10):
        """
        But : créer la raquette en bas du canvas et lier le clavier et la
        souris.
        Entrées :
            canvas (tk.Canvas) : zone de jeu.
            largeur, hauteur (int) : dimensions de la raquette.
            vitesse (int) : pas de déplacement au clavier.
        Sortie : aucune.
        """
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
        self.vitesse = vitesse
        self.x = (self.canvas.winfo_width() - self.largeur) / 2
        self.y = self.canvas.winfo_height() - self.hauteur - 10
        self.id = self.canvas.create_rectangle(self.x, self.y,
                                               self.x + self.largeur,
                                               self.y + self.hauteur,
                                               fill="#2de2e6",
                                               outline="#ff6ad5", width=2)
        self.canvas.bind("<Left>", self.deplacer_gauche)
        self.canvas.bind("<Right>", self.deplacer_droite)
        self.canvas.bind("<Motion>", self.suivre_souris)
        self.canvas.focus_set()

    def deplacer_gauche(self, event):
        """
        But : décaler la raquette vers la gauche sans sortir du canvas.
        Entrée : event (tk.Event) : appui sur la flèche gauche.
        Sortie : aucune.
        """
        if self.x - self.vitesse >= 0:
            self.x -= self.vitesse
            self.canvas.move(self.id, -self.vitesse, 0)

    def deplacer_droite(self, event):
        """
        But : décaler la raquette vers la droite sans sortir du canvas.
        Entrée : event (tk.Event) : appui sur la flèche droite.
        Sortie : aucune.
        """
        if self.x + self.largeur + self.vitesse <= self.canvas.winfo_width():
            self.x += self.vitesse
            self.canvas.move(self.id, self.vitesse, 0)

    def suivre_souris(self, event):
        """
        But : placer la raquette sous la souris.
        Entrée : event (tk.Event) : mouvement de la souris.
        Sortie : aucune.
        """
        if 0 <= event.x <= self.canvas.winfo_width() - self.largeur:
            self.x = event.x
            self.canvas.coords(self.id, self.x, self.y,
                               self.x + self.largeur, self.y + self.hauteur)
