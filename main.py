# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Lancer le jeu 

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Enregitrer le meilleur score avec nom dans le fichier score.txt .
"""

from jeu.application import Application


if __name__ == "__main__":
    app = Application()
    app.lancer()
