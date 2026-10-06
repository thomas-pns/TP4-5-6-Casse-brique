# Header
# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Point d'entrée du programme, instancie Application et lance la boucle principale (mainloop).

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Gestion arguments ligne de commande (--fullscreen, --level), profil de performance, logs.
"""

from jeu.application import Application


if __name__ == "__main__":
    app = Application()
    app.lancer()