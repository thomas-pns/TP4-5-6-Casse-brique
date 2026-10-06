# Header
# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Gérer la fenêtre principale, menu de démarrage, affichage score/vies.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Menu pause, écran game over, redimensionnement fenêtre, paramètres.
"""
import tkinter as tk
from tkinter import messagebox

class Application:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse Brique")
        self.fenetre.geometry("800x600")

        self.create_menu()
        self.creer_widgets()



    def creer_widgets(self):
        self.canvas = tk.Canvas(self.fenetre, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.fenetre.configure(bg="black")

        self.texte_score = self.canvas.create_text(700, 20, text="Score : 0", fill="yellow", font=("Helvetica", 14, "bold"))
        self.label_vies = self.canvas.create_text(100, 20, text="Vies : 3", fill="red", font=("Helvetica", 14, "bold"))



        tk.Button(self.fenetre, text="Démarrer").pack()
        tk.Button(self.fenetre, text="QUITTER", fg="red", command=self.fenetre.destroy).pack()

    def create_menu(self):
        barre = tk.Menu(self.fenetre)
        menu_aide= tk.Menu(barre, tearoff=0)
        menu_aide.add_command(label="Règles du jeu", command=self.afficher_regles)
        barre.add_cascade(label="Aide", menu=menu_aide)
        self.fenetre.config(menu=barre)

    def afficher_regles(self):
        tk.messagebox.showinfo("Règles", "Détruisez toutes les briques !", parent=self.fenetre)

    def lancer(self):
        self.fenetre.mainloop()
