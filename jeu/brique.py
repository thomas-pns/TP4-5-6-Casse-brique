# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Classe de base Brique (position, vie, points, couleur), sous-classe
    BriqueNormale, et fonction creer_grille qui dessine un niveau de briques
    sur un canvas.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    BriqueSolide (2 coups), BriqueIndestructible, BriqueBonus,
    brique explosive, drop power-up.
"""

import tkinter as tk
import random
from structures.liste import Liste


LARGEUR_CANVAS = 500
HAUTEUR_CANVAS = 400
NB_LIGNES = 5
NB_COLONNES = 8
LARGEUR_BRIQUE = 50
HAUTEUR_BRIQUE = 20
ESPACEMENT = 5
MARGE_HAUT = 40
COULEUR_INTERIEUR = "#12002b"
EPAISSEUR_NEON = 2
COULEURS_NEON = ["#ffb000", "#ff2bd6", "#c03cff", "#4d6bff", "#00e5ff"]

NB_ECLATS = 12
TAILLE_ECLAT = 8
NB_IMAGES = 15
PERIODE_ECLATS_MS = 30
GRAVITE = 0.5
RETRECISSEMENT = 0.95
MOTIFS_FONDU = ["", "", "gray75", "gray50", "gray25"]

class Brique:
    """
    Classe de base des briques du jeu.
    Attributs :
        x, y : coin supérieur gauche (pixels, l'axe y est orienté vers le bas).
        largeur, hauteur : dimensions (pixels).
        vie : nombre de coups restants avant destruction.
        points : points attribués à la destruction.
        couleur : couleur de base.
        type_bonus : bonus libéré à la destruction (None si aucun).
        id_canvas : identifiant Tkinter du rectangle (None si non dessinée).
    """

    def __init__(self, x, y, largeur, hauteur, vie, points, couleur):
        """
        But : initialiser une brique.
        Entrées :
            x, y (int) : position du coin supérieur gauche.
            largeur, hauteur (int) : dimensions.
            vie (int) : coups nécessaires pour la détruire.
            points (int) : points gagnés à la destruction.
            couleur (str) : couleur Tkinter de base.
        Sortie : aucune.
        """
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.vie = vie
        self.points = points
        self.couleur = couleur
        self.type_bonus = None
        self.id_canvas = None

    def est_detruite(self):
        """
        But : indiquer si la brique n'a plus de vie.
        Entrée : aucune.
        Sortie : (bool) True si vie <= 0, False sinon.
        """
        return self.vie <= 0

    def frapper(self):
        """
        But : appliquer un coup de balle à la brique.
        Entrée : aucune.
        Sortie : (bool) True si la brique est détruite par ce coup.
        """
        self.vie -= 1
        return self.est_detruite()

    def couleur_actuelle(self):
        """
        But : donner la couleur d'affichage (redéfinie si elle dépend de
        la vie).
        Entrée : aucune.
        Sortie : (str) couleur Tkinter.
        """
        return self.couleur

    def obtenir_boite(self):
        """
        But : fournir le rectangle englobant, utile aux tests de collision.
        Entrée : aucune.
        Sortie : (tuple) (x_min, y_min, x_max, y_max).
        """
        return (self.x, self.y, self.x + self.largeur, self.y + self.hauteur)

    def dessiner(self, canvas):
        """
        But : créer le rectangle de la brique sur le canvas.
        Entrée : canvas (tk.Canvas) : zone de jeu.
        Sortie : aucune (l'identifiant Tkinter est stocké dans id_canvas).
        """
        x_min, y_min, x_max, y_max = self.obtenir_boite()
        self.id_canvas = canvas.create_rectangle(
            x_min, y_min, x_max, y_max,
            fill=self.couleur_actuelle(), stipple="gray25",
            outline=self.couleur_actuelle(), width=EPAISSEUR_NEON
        )

    def rafraichir(self, canvas):
        """
        But : mettre à jour la couleur après un coup non fatal.
        Entrée : canvas (tk.Canvas) : zone de jeu.
        Sortie : aucune.
        """
        canvas.itemconfig(self.id_canvas, fill=self.couleur_actuelle(),
                          outline=self.couleur_actuelle())

    def effacer(self, canvas):
        """
        But : retirer la brique du canvas.
        Entrée : canvas (tk.Canvas) : zone de jeu.
        Sortie : aucune.
        """
        canvas.delete(self.id_canvas)
        self.id_canvas = None

    def __str__(self):
        """
        But : représentation textuelle pour le débogage.
        Entrée : aucune.
        Sortie : (str) description de la brique.
        """
        return (f"{type(self).__name__}(vie={self.vie}, "
                f"points={self.points}, couleur={self.couleur})")


class BriqueNormale(Brique):
    """Brique détruite en un coup."""

    def __init__(self, x, y, largeur, hauteur):
        """
        But : créer une brique normale (1 coup, 10 points).
        Entrées :
            x, y (int) : position du coin supérieur gauche.
            largeur, hauteur (int) : dimensions.
        Sortie : aucune.
        """
        super().__init__(x, y, largeur, hauteur,
                         vie=1, points=10, couleur="green")

class Explosion:
    """
    Animation de destruction d'une brique : des éclats de sa couleur
    partent dans tous les sens, retombent et s'estompent.
    Attributs :
        canvas : zone de jeu.
        eclats : liste de [identifiant, vitesse_x, vitesse_y].
        image : numéro de l'image en cours.
    """

    def __init__(self, canvas, brique):
        """
        But : créer les éclats sur la brique et lancer l'animation.
        Entrées :
            canvas (tk.Canvas) : zone de jeu.
            brique (Brique) : brique qui vient d'être détruite.
        Sortie : aucune.
        """
        self.canvas = canvas
        self.eclats = []
        self.image = 0
        x_min, y_min, x_max, y_max = brique.obtenir_boite()
        couleur = brique.couleur_actuelle()
        for _ in range(NB_ECLATS):
            x = random.uniform(x_min, x_max - TAILLE_ECLAT)
            y = random.uniform(y_min, y_max - TAILLE_ECLAT)
            id_eclat = canvas.create_rectangle(x, y, x + TAILLE_ECLAT,
                                               y + TAILLE_ECLAT,
                                               fill=couleur, outline="")
            vitesse_x = random.uniform(-5, 5)
            vitesse_y = random.uniform(-6, 0)
            self.eclats.append([id_eclat, vitesse_x, vitesse_y])
        self.animer()

    def animer(self):
        """
        But : faire avancer les éclats d'une image, puis se relancer
        jusqu'à la fin de l'animation, où les éclats sont supprimés.
        Entrée : aucune.
        Sortie : aucune.
        """
        if self.image >= NB_IMAGES:
            for eclat in self.eclats:
                self.canvas.delete(eclat[0])
            return

        motif = MOTIFS_FONDU[self.image * len(MOTIFS_FONDU) // NB_IMAGES]
        for eclat in self.eclats:
            id_eclat, vitesse_x, vitesse_y = eclat
            self.canvas.move(id_eclat, vitesse_x, vitesse_y)
            coords = self.canvas.coords(id_eclat)
            if coords:
                centre_x = (coords[0] + coords[2]) / 2
                centre_y = (coords[1] + coords[3]) / 2
                self.canvas.scale(id_eclat, centre_x, centre_y,
                                  RETRECISSEMENT, RETRECISSEMENT)
            self.canvas.itemconfigure(id_eclat, stipple=motif)
            eclat[2] = vitesse_y + GRAVITE
        self.image += 1
        self.canvas.after(PERIODE_ECLATS_MS, self.animer)


def fabriquer_brique(ligne, colonne, x, y):
    """
    But : créer la brique d'une case de la grille.
    Entrées :
        ligne (int) : indice de ligne, qui fixe la couleur néon.
        colonne (int) : indice de colonne (inutilisé pour l'instant,
        prévu pour varier les types de briques).
        x, y (int) : position du coin supérieur gauche (pixels).
    Sortie : (Brique) la brique créée.
    """
    brique = BriqueNormale(x, y, LARGEUR_BRIQUE, HAUTEUR_BRIQUE)
    # Couleur néon selon la ligne, en dégradé comme le ciel du fond.
    # Le modulo évite une IndexError si NB_LIGNES dépasse 5.
    brique.couleur = COULEURS_NEON[ligne % len(COULEURS_NEON)]
    return brique


def creer_grille(canvas, largeur_canvas=LARGEUR_CANVAS):
    """
    But : construire la grille de briques, centrée, et la dessiner.
    Entrées :
        canvas (tk.Canvas) : zone de jeu sur laquelle dessiner.
        largeur_canvas (int) : largeur du canvas, pour centrer la grille.
    Sortie : (Liste) les briques créées, dans l'ordre de la grille.
    """
    briques = Liste()
    largeur_grille = (NB_COLONNES * LARGEUR_BRIQUE +
                      (NB_COLONNES - 1) * ESPACEMENT)
    decalage = (largeur_canvas - largeur_grille) // 2
    for indice in range(NB_LIGNES * NB_COLONNES):
        ligne, colonne = divmod(indice, NB_COLONNES)
        x = decalage + colonne * (LARGEUR_BRIQUE + ESPACEMENT)
        y = MARGE_HAUT + ligne * (HAUTEUR_BRIQUE + ESPACEMENT)
        brique = fabriquer_brique(ligne, colonne, x, y)
        brique.dessiner(canvas)
        briques.ajouter_fin(brique)
    return briques


def trouver_brique(briques, x, y):
    """
    But : renvoyer la brique qui contient le point (x, y).
    Entrées :
        briques (Liste) : briques encore présentes.
        x, y (int) : coordonnées du point (pixels).
    Sortie : (Brique ou None) la brique trouvée, None si aucune.
    """
    for brique in briques:
        x_min, y_min, x_max, y_max = brique.obtenir_boite()
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return brique
    return None


if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("Test des briques : cliquez dessus")
    zone = tk.Canvas(fenetre, width=LARGEUR_CANVAS, height=HAUTEUR_CANVAS,
                     bg="black")
    zone.pack()
    grille = creer_grille(zone)

    def cliquer(evenement):
        """Frappe la brique sous le clic, la retire si elle est détruite."""
        brique = trouver_brique(grille, evenement.x, evenement.y)
        if brique is None:
            return
        if brique.frapper():
            brique.effacer(zone)
            grille.supprimer(brique)
            print("Détruite :", brique, "| restantes :", len(grille))
        else:
            brique.rafraichir(zone)
            print("Touchée :", brique)

    zone.bind("<Button-1>", cliquer)
    fenetre.mainloop()
