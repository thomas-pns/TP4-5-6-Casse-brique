# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Gérer la fenêtre principale, menu de démarrage, affichage score/vies.

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Menu pause, redimensionnement fenêtre, paramètres.
"""

import os
import tkinter as tk
from tkinter import messagebox

from jeu.balle import Balle
from jeu.brique import creer_grille
from jeu.partie import Partie
from jeu.raquette import Raquette


TAG_GAME_OVER = "game_over"
TAG_FOND = "fond"
CHEMIN_FOND = os.path.join(os.path.dirname(__file__), "..", "data",
                           "fond.png")


class Application:
    """
    Fenêtre principale du jeu.
    Attributs :
        fenetre : fenêtre Tk.
        canvas : zone de jeu.
        image_fond : image de fond.
        texte_score, label_vies : textes du score et des vies.
        boutons_game_over : boutons de l'écran game over.
    """

    def __init__(self):
        """
        But : créer la fenêtre, le menu et les widgets.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse Brique")
        self.fenetre.geometry("800x600")

        self.create_menu()
        self.creer_widgets()

    def creer_widgets(self):
        """
        But : créer le canvas, le fond, le score, les vies et les boutons.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.canvas = tk.Canvas(self.fenetre, bg="black",
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.fenetre.configure(bg="black")

        self.image_fond = tk.PhotoImage(file=CHEMIN_FOND)
        self.creer_fond()
        self.creer_hud()

        tk.Button(self.fenetre, text="Démarrer", command=self.test).pack()
        tk.Button(self.fenetre, text="QUITTER", fg="red",
                  command=self.fenetre.destroy).pack()

    def creer_hud(self):
        """
        But : dessiner les textes du score et des vies en haut du canvas.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.texte_score = self.canvas.create_text(
            700, 20, text="Score : 0", fill="yellow",
            font=("Helvetica", 14, "bold"))
        self.label_vies = self.canvas.create_text(
            100, 20, text="Vies : 3", fill="red",
            font=("Helvetica", 14, "bold"))

    def afficher_vies(self, nombre):
        """
        But : mettre à jour le nombre de vies affiché.
        Entrée : nombre (int) : vies restantes.
        Sortie : aucune.
        """
        self.canvas.itemconfigure(self.label_vies, text=f"Vies : {nombre}")

    def create_menu(self):
        """
        But : créer la barre de menu avec le menu Aide.
        Entrée : aucune.
        Sortie : aucune.
        """
        barre = tk.Menu(self.fenetre)
        menu_aide = tk.Menu(barre, tearoff=0)
        menu_aide.add_command(label="Règles du jeu",
                              command=self.afficher_regles)
        barre.add_cascade(label="Aide", menu=menu_aide)
        self.fenetre.config(menu=barre)

    def afficher_game_over(self, score):
        """
        But : superposer l'écran game over au jeu (titre, score
        final, boutons Rejouer et Quitter).
        Entrée : score (int) : score final de la partie.
        Sortie : aucune.
        """
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()
        centre_x = largeur / 2
        centre_y = hauteur / 2

        # Le canvas Tk ne gère pas la transparence : le motif gray50 ne
        # peint qu'un pixel sur deux, ce qui assombrit le jeu en dessous.
        self.canvas.create_rectangle(0, 0, largeur, hauteur, fill="black",
                                     stipple="gray50", outline="",
                                     tags=TAG_GAME_OVER)
        self.canvas.create_text(centre_x, centre_y - 60, text="GAME OVER",
                                fill="red", font=("Helvetica", 48, "bold"),
                                tags=TAG_GAME_OVER)
        self.canvas.create_text(centre_x, centre_y + 5,
                                text=f"Score final : {score}", fill="yellow",
                                font=("Helvetica", 20, "bold"),
                                tags=TAG_GAME_OVER)

        bouton_rejouer = tk.Button(self.canvas, text="Rejouer", width=10,
                                   command=self.rejouer)
        bouton_quitter = tk.Button(self.canvas, text="Quitter", width=10,
                                   fg="red", command=self.fenetre.destroy)
        self.canvas.create_window(centre_x - 70, centre_y + 70,
                                  window=bouton_rejouer, tags=TAG_GAME_OVER)
        self.canvas.create_window(centre_x + 70, centre_y + 70,
                                  window=bouton_quitter, tags=TAG_GAME_OVER)
        self.boutons_game_over = [bouton_rejouer, bouton_quitter]

        # Entrée relance aussi la partie.
        self.canvas.bind("<Return>", lambda evenement: self.rejouer())
        self.canvas.focus_set()

    def rejouer(self):
        """
        But : effacer l'écran game over et le niveau est terminé, puis relancer
        une nouvelle partie.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.canvas.unbind("<Return>")
        # delete("all") retire les fenêtres du canvas, pas les widgets
        # eux-mêmes : on détruit donc les boutons explicitement.
        for bouton in self.boutons_game_over:
            bouton.destroy()
        self.boutons_game_over = []

        self.canvas.delete("all")
        self.creer_fond()
        self.creer_hud()
        self.test()

    def afficher_regles(self):
        """
        But : afficher les règles du jeu dans une fenêtre d'information.
        Entrée : aucune.
        Sortie : aucune.
        """
        messagebox.showinfo("Règles", "Détruisez toutes les briques !",
                            parent=self.fenetre)

    def lancer(self):
        """
        But : lancer la boucle principale Tkinter.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.fenetre.mainloop()

    def test(self):
        """
        But : créer la balle, la raquette et les briques, puis démarrer
        une partie.
        Entrée : aucune.
        Sortie : aucune.
        """
        balle = Balle(self.canvas, x=400, y=300, rayon=10, vitesse_x=5,
                      vitesse_y=5)
        raquette = Raquette(self.canvas)
        briques = creer_grille(self.canvas, largeur_canvas=800)

        partie = Partie(self, self.canvas, balle, raquette, briques, 0)
        partie.boucle_jeu()

    def afficher_score(self, score):
        """
        But : mettre à jour le score affiché.
        Entrée : score (int) : score courant.
        Sortie : aucune.
        """
        self.canvas.itemconfigure(self.texte_score, text=f"Score : {score}")

    def creer_fond(self):
        """
        But : dessiner l'image de fond et la placer sous tous les autres
        éléments du canvas.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.canvas.create_image(0, 0, image=self.image_fond, anchor="nw",
                                 tags=TAG_FOND)
        self.canvas.tag_lower(TAG_FOND)


if __name__ == "__main__":
    app = Application()
    app.lancer()
