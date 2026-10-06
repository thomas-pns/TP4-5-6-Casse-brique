# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Définir la raquette (position, dimensions, vitesse), gérer déplacements clavier/souris, limiter aux bords écran.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Raquette qui s'agrandit/rétrécit, effet "collant", visuel particules.
"""

import tkinter as tk

class Raquette(): 
    def __init__(self, canvas, largeur=100, hauteur=20, vitesse=10):
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
        self.vitesse = vitesse
        self.x = (self.canvas.winfo_width() - self.largeur) / 2
        self.y = self.canvas.winfo_height() - self.hauteur - 10
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill="blue")
        self.canvas.bind("<Left>", self.deplacer_gauche)
        self.canvas.bind("<Right>", self.deplacer_droite)
        self.canvas.bind("<Motion>", self.suivre_souris)
        self.canvas.focus_set()

    def deplacer_gauche(self, event):
        if self.x - self.vitesse >= 0:
            self.x -= self.vitesse
            self.canvas.move(self.rect, -self.vitesse, 0)
    def deplacer_droite(self, event):
        if self.x + self.largeur + self.vitesse <= self.canvas.winfo_width():
            self.x += self.vitesse
            self.canvas.move(self.rect, self.vitesse, 0)
    def suivre_souris(self, event):
        if 0 <= event.x <= self.canvas.winfo_width() - self.largeur:
            self.x = event.x
            self.canvas.coords(self.rect, self.x, self.y, self.x + self.largeur, self.y + self.hauteur)