# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Définir la balle (position, vitesse, rayon), gérer physique rebonds,
    réinitialisation après vie perdue.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Vitesse progressive, balle traversante, multi-balles.
"""
from structures.file import File


LONGUEUR_TRAINEE = 8
# Du plus ancien (sombre) au plus récent (proche de la balle).
COULEURS_TRAINEE = ["#2a0845", "#45106b", "#62188f", "#8a1fb0",
                    "#b026c9", "#d62ed8", "#f040de", "#ff6ad5"]

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
        self.trainee = File()

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
        self.ajouter_trace()
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.canvas.move(self.id, self.vitesse_x, self.vitesse_y)

        if self.x + self.rayon >= self.canvas.winfo_width():
            self.vitesse_x = -self.vitesse_x
        if self.x - self.rayon <= 0:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.rayon <= 0:
            self.vitesse_y = -self.vitesse_y

    def ajouter_trace(self):
        """
        But : laisser une trace à la position actuelle de la balle et
        retirer la plus ancienne quand la traînée est trop longue.
        Entrée : aucune.
        Sortie : aucune.
        """
        id_trace = self.canvas.create_oval(0, 0, 0, 0, outline="")
        # Juste sous la balle, mais au-dessus du fond et des briques.
        self.canvas.tag_lower(id_trace, self.id)
        self.trainee.enfiler((id_trace, self.x, self.y))
        if len(self.trainee) > LONGUEUR_TRAINEE:
            id_ancien = self.trainee.defiler()[0]
            self.canvas.delete(id_ancien)

        # Plus une trace est ancienne, plus elle est petite et sombre.
        decalage = LONGUEUR_TRAINEE - len(self.trainee)
        for rang, (id_trace, x, y) in enumerate(self.trainee):
            niveau = rang + decalage
            rayon = self.rayon * (niveau + 1) / (LONGUEUR_TRAINEE + 1)
            self.canvas.coords(id_trace, x - rayon, y - rayon,
                               x + rayon, y + rayon)
            self.canvas.itemconfigure(id_trace,
                                      fill=COULEURS_TRAINEE[niveau])

    def effacer_trainee(self):
        """
        But : supprimer toutes les traces (vie perdue ou fin de partie).
        Entrée : aucune.
        Sortie : aucune.
        """
        while not self.trainee.est_vide():
            id_trace = self.trainee.defiler()[0]
            self.canvas.delete(id_trace)