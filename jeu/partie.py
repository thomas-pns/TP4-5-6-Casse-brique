# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Orchestrer la boucle de jeu, détecter collisions (balle/raquette,
    balle/briques, balle/murs), gérer fin de partie (victoire/défaite).

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Power-ups, niveaux multiples, système de combo, sauvegarde/reprise partie.
"""
import math


ANGLE_NORMALE_MAX = math.radians(30)
ANGLE_MAX_VERTICALE = math.radians(70)

class Partie:
    """
    Gère la boucle de jeu et les collisions.
    Attributs :
        fenetre : fenêtre Tk (pour programmer la boucle avec after).
        canvas : zone de jeu.
        balle : balle en jeu.
        raquette : raquette du joueur.
        briques : Liste des briques encore présentes.
        score : points accumulés.
    """

    def __init__(self, application, canvas, balle, raquette, briques, score):
        """
        But : initialiser une partie.
        Entrées :
            fenetre (tk.Tk) : fenêtre principale.
            canvas (tk.Canvas) : zone de jeu.
            balle (Balle) : balle en jeu.
            raquette (Raquette) : raquette du joueur.
            briques (Liste) : briques du niveau.
            score (int) : score de départ.
        Sortie : aucune.
        """
        self.application = application
        self.canvas = canvas
        self.balle = balle
        self.raquette = raquette
        self.briques = briques
        self.score = score

        self.vies = 3
        self.application.afficher_vies(self.vies)

        
    def lecture_coords(self):
        coords_balle = self.canvas.coords(self.balle.id)
        coords_raquette = self.canvas.coords(self.raquette.id)
        # print(coords_raquette, coords_balle)

        return coords_balle, coords_raquette


    def verifier_collisions(self):
        coords_balle, coords_raquette = self.lecture_coords()
        x1, y1, x2, y2 = coords_balle
        rx1, ry1, rx2, ry2 = coords_raquette

        if x1 <= rx2 and x2 >= rx1 and y2 >= ry1 and y1 <= ry2:
            self.rebond_raquette(rx1, rx2)
            print("Collision détectée !")

        self.gerer_collision_briques()

    def rebond_raquette(self, rx1, rx2):
        centre = (rx1 + rx2) / 2
        demi_largeur = (rx2 - rx1) / 2
        decalage = (self.balle.x - centre) / demi_largeur
        decalage = max(-1.0, min(1.0, decalage))
    
          # Normale locale de la raquette, inclinée selon le point d'impact.
        alpha = decalage * ANGLE_NORMALE_MAX
        normale_x = math.sin(alpha)
        normale_y = -math.cos(alpha)
    
        # Réflexion de Descartes : v' = v - 2 (v.n) n, si la balle arrive
        # bien vers la raquette (v.n < 0).
        produit = (self.balle.vitesse_x * normale_x
                   + self.balle.vitesse_y * normale_y)
        if produit < 0:
            self.balle.vitesse_x -= 2 * produit * normale_x
            self.balle.vitesse_y -= 2 * produit * normale_y
    
            # Garde-fou : la balle repart vers le haut, à au plus 70° de la
            # verticale, avec la même norme de vitesse.
        norme = math.hypot(self.balle.vitesse_x, self.balle.vitesse_y)
        angle = math.atan2(self.balle.vitesse_x, -self.balle.vitesse_y)
        angle = max(-ANGLE_MAX_VERTICALE, min(ANGLE_MAX_VERTICALE, angle))
        self.balle.vitesse_x = norme * math.sin(angle)
        self.balle.vitesse_y = -norme * math.cos(angle)
    
    def perdre_une_vie(self):
        print("Vie perdue !")
        print(f"Vies restantes : {self.vies}")
        self.vies -= 1
        print(f"Vies restantes après perte : {self.vies}")
        self.application.afficher_vies(self.vies)

        self.balle.x = 400
        self.balle.y = 300
        self.balle.vitesse_x = 5
        self.balle.vitesse_y = 5
        self.canvas.coords(self.balle.id, self.balle.x - self.balle.rayon, self.balle.y - self.balle.rayon, self.balle.x + self.balle.rayon, self.balle.y + self.balle.rayon)

    def boucle_jeu(self):
        # print("Boucle de jeu en cours...")
        self.balle.deplacer()

        if self.balle.est_tombee():
            # print("La balle est tombée ! Vie perdue.")
            self.perdre_une_vie()

            if self.vies <= 0:
                print("Partie terminée !")
                return

        else:
            self.verifier_collisions()

        self.application.fenetre.after(20, lambda: self.boucle_jeu())