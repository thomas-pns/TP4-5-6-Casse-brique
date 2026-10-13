# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Structures de données du jeu : Liste chaînée, Pile (LIFO) et File (FIFO).

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 13/10/2026

ToDo List:
    Tests unitaires, accès par indice, insertion au milieu.
"""


class Noeud:
    """
    Maillon d'une liste chaînée.
    Attributs :
        valeur : donnée stockée.
        suivant : maillon suivant (None en fin de liste).
    """

    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant


class Liste:
    """
    Liste simplement chaînée avec pointeurs de tête et de queue.
    Attributs :
        tete, queue : premier et dernier maillons (None si vide).
        taille : nombre d'éléments.
    """

    def __init__(self):
        self.tete = None
        self.queue = None
        self.taille = 0

    def est_vide(self):
        """
        But : tester si la liste est vide.
        Entrée : aucune.
        Sortie : (bool) True si aucun élément.
        """
        return self.tete is None

    def ajouter_debut(self, valeur):
        """
        But : insérer un élément en tête (coût constant).
        Entrée : valeur (object) : élément à insérer.
        Sortie : aucune.
        """
        noeud = Noeud(valeur, self.tete)
        self.tete = noeud
        if self.queue is None:
            self.queue = noeud
        self.taille += 1

    def ajouter_fin(self, valeur):
        """
        But : insérer un élément en queue (coût constant).
        Entrée : valeur (object) : élément à insérer.
        Sortie : aucune.
        """
        noeud = Noeud(valeur)
        if self.queue is None:
            self.tete = noeud
        else:
            self.queue.suivant = noeud
        self.queue = noeud
        self.taille += 1

    def retirer_debut(self):
        """
        But : retirer et renvoyer le premier élément (coût constant).
        Entrée : aucune.
        Sortie : (object) valeur retirée.
        Lève IndexError si la liste est vide.
        """
        if self.tete is None:
            raise IndexError("Retrait impossible : structure vide")
        noeud = self.tete
        self.tete = noeud.suivant
        if self.tete is None:
            self.queue = None
        self.taille -= 1
        return noeud.valeur

    def supprimer(self, valeur):
        """
        But : supprimer la première occurrence d'un objet (comparaison par
        identité, adaptée à des objets comme les briques). Coût linéaire.
        Entrée : valeur (object) : objet à supprimer.
        Sortie : (bool) True si l'objet a été trouvé et supprimé.
        """
        precedent = None
        courant = self.tete
        while courant is not None:
            if courant.valeur is valeur:
                if precedent is None:
                    self.tete = courant.suivant
                else:
                    precedent.suivant = courant.suivant
                if courant is self.queue:
                    self.queue = precedent
                self.taille -= 1
                return True
            precedent = courant
            courant = courant.suivant
        return False

    def __iter__(self):
        """
        But : parcourir les valeurs de la tête vers la queue.
        Entrée : aucune.
        Sortie : (générateur) valeurs successives.
        """
        courant = self.tete
        while courant is not None:
            yield courant.valeur
            courant = courant.suivant

    def __len__(self):
        return self.taille


class Pile:
    """Pile (LIFO) : le dernier élément empilé est le premier dépilé."""

    def __init__(self):
        self.elements = Liste()

    def empiler(self, valeur):
        """
        But : ajouter un élément au sommet.
        Entrée : valeur (object). Sortie : aucune.
        """
        self.elements.ajouter_debut(valeur)

    def depiler(self):
        """
        But : retirer et renvoyer l'élément du sommet.
        Entrée : aucune. Sortie : (object) élément retiré.
        Lève IndexError si la pile est vide.
        """
        return self.elements.retirer_debut()

    def sommet(self):
        """
        But : consulter le sommet sans le retirer.
        Entrée : aucune. Sortie : (object) élément du sommet.
        Lève IndexError si la pile est vide.
        """
        if self.elements.est_vide():
            raise IndexError("Pile vide")
        return self.elements.tete.valeur

    def est_vide(self):
        return self.elements.est_vide()

    def __len__(self):
        return len(self.elements)


class File:
    """File (FIFO) : le premier élément enfilé est le premier défilé."""

    def __init__(self):
        self.elements = Liste()

    def enfiler(self, valeur):
        """
        But : ajouter un élément en fin de file.
        Entrée : valeur (object). Sortie : aucune.
        """
        self.elements.ajouter_fin(valeur)

    def defiler(self):
        """
        But : retirer et renvoyer l'élément en tête de file.
        Entrée : aucune. Sortie : (object) élément retiré.
        Lève IndexError si la file est vide.
        """
        return self.elements.retirer_debut()

    def est_vide(self):
        return self.elements.est_vide()

    def __len__(self):
        return len(self.elements)


