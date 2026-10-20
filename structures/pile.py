# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Implémenter pile LIFO (empiler/dépiler/sommet/vide).

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
"""

from structures.liste import Liste


class Pile:
    """Pile (LIFO) : le dernier élément empilé est le premier dépilé."""

    def __init__(self):
        """
        But : créer une pile vide.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.elements = Liste()

    def empiler(self, valeur):
        """
        But : ajouter un élément au sommet.
        Entrée : valeur (object) : élément à empiler.
        Sortie : aucune.
        """
        self.elements.ajouter_debut(valeur)

    def depiler(self):
        """
        But : retirer et renvoyer l'élément du sommet.
        Entrée : aucune.
        Sortie : (object) élément retiré.
        Lève IndexError si la pile est vide.
        """
        return self.elements.retirer_debut()

    def sommet(self):
        """
        But : consulter le sommet sans le retirer.
        Entrée : aucune.
        Sortie : (object) élément du sommet.
        Lève IndexError si la pile est vide.
        """
        if self.elements.est_vide():
            raise IndexError("Pile vide")
        return self.elements.tete.valeur

    def est_vide(self):
        """
        But : tester si la pile est vide.
        Entrée : aucune.
        Sortie : (bool) True si aucun élément.
        """
        return self.elements.est_vide()

    def __len__(self):
        """
        But : donner le nombre d'éléments.
        Entrée : aucune.
        Sortie : (int) nombre d'éléments.
        """
        return len(self.elements)
