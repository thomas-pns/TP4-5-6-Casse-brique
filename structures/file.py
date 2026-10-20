# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Implémenter file FIFO (enfiler/défiler/tête/vide), utiliser pour file
    d'événements ou power-ups en attente.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    File circulaire, file de priorité, persistance, itérateur.
"""

from structures.liste import Liste


class File:
    """File (FIFO) : le premier élément enfilé est le premier défilé."""

    def __init__(self):
        """
        But : créer une file vide.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.elements = Liste()

    def enfiler(self, valeur):
        """
        But : ajouter un élément en fin de file.
        Entrée : valeur (object) : élément à ajouter.
        Sortie : aucune.
        """
        self.elements.ajouter_fin(valeur)

    def defiler(self):
        """
        But : retirer et renvoyer l'élément en tête de file.
        Entrée : aucune.
        Sortie : (object) élément retiré.
        Lève IndexError si la file est vide.
        """
        return self.elements.retirer_debut()

    def est_vide(self):
        """
        But : tester si la file est vide.
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

    def __iter__(self):
        """
        But : parcourir la file, du premier élément entré au dernier.
        Entrée : aucune.
        Sortie : (générateur) éléments successifs.
        """
        return iter(self.elements)
