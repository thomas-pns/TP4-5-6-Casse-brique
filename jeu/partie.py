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

from jeu.brique import Explosion

ANGLE_NORMALE_MAX = math.radians(30)
ANGLE_MAX_VERTICALE = math.radians(70)


class Partie:
    """
    Gère la boucle de jeu et les collisions.
    Attributs :
        application : application qui affiche le jeu.
        canvas : zone de jeu.
        balle : balle en jeu.
        raquette : raquette du joueur.
        briques : Liste des briques encore présentes.
        score : points accumulés.
        vies : vies restantes.
        est_terminee : True quand la partie est finie.
    """

    def __init__(self, application, canvas, balle, raquette, briques, score):
        """
        But : initialiser une partie.
        Entrées :
            application (Application) : application qui affiche le jeu.
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
        self.est_terminee = False
        self.application.afficher_score(self.score)

    def lecture_coords(self):
        """
        But : lire les coordonnées de la balle et de la raquette.
        Entrée : aucune.
        Sortie : (tuple) (coords_balle, coords_raquette).
        """
        coords_balle = self.canvas.coords(self.balle.id)
        coords_raquette = self.canvas.coords(self.raquette.id)

        return coords_balle, coords_raquette

    def verifier_collisions(self):
        """
        But : gérer le contact de la balle avec la raquette puis avec les
        briques.
        Entrée : aucune.
        Sortie : aucune.
        """
        coords_balle, coords_raquette = self.lecture_coords()
        x1, y1, x2, y2 = coords_balle
        rx1, ry1, rx2, ry2 = coords_raquette

        if x1 <= rx2 and x2 >= rx1 and y2 >= ry1 and y1 <= ry2:
            self.rebond_raquette(rx1, rx2)

        self.gerer_collision_briques()

    def rebond_raquette(self, rx1, rx2):
        """
        But : faire rebondir la balle sur la raquette, avec un angle qui
        dépend du point d'impact.
        Entrées :
            rx1, rx2 (float) : bords gauche et droit de la raquette.
        Sortie : aucune (modifie la vitesse de la balle).
        """
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
        produit = (self.balle.vitesse_x * normale_x +
                   self.balle.vitesse_y * normale_y)
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
        """
        But : retirer une vie et remettre la balle au centre.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.vies -= 1
        self.application.afficher_vies(self.vies)
        self.balle.effacer_trainee()

        self.balle.x = 400
        self.balle.y = 300
        self.balle.vitesse_x = 5
        self.balle.vitesse_y = 5
        self.canvas.coords(self.balle.id,
                           self.balle.x - self.balle.rayon,
                           self.balle.y - self.balle.rayon,
                           self.balle.x + self.balle.rayon,
                           self.balle.y + self.balle.rayon)

    def boucle_jeu(self):
        """
        But : faire avancer le jeu d'un pas, puis se relancer toutes les
        20 ms tant que la partie n'est pas finie.
        Entrée : aucune.
        Sortie : aucune.
        """
        if self.est_terminee:
            return

        self.balle.deplacer()

        if self.balle.est_tombee():
            self.perdre_une_vie()

            if self.vies <= 0:
                self.terminer()
                return

        else:
            self.verifier_collisions()

        self.application.fenetre.after(20, lambda: self.boucle_jeu())

    def terminer(self):
        """
        But : arrêter la partie (défaite) et afficher l'écran game over.
        Entrée : aucune.
        Sortie : aucune.
        """
        self.est_terminee = True
        self.balle.effacer_trainee()
        self.canvas.delete(self.balle.id)
        self.application.afficher_game_over(self.score)

    def point_le_plus_proche(self, brique):
        """
        But : trouver le point de la brique le plus proche du centre de la
        balle (projection du centre sur le rectangle, axe par axe).
        Entrée : brique (Brique) : brique testée.
        Sortie : (tuple) (x_proche, y_proche).
        """
        x_min, y_min, x_max, y_max = brique.obtenir_boite()
        x_proche = min(max(self.balle.x, x_min), x_max)
        y_proche = min(max(self.balle.y, y_min), y_max)
        return x_proche, y_proche

    def touche(self, brique):
        """
        But : tester si la balle (disque) chevauche une brique.
        Entrée : brique (Brique) : brique testée.
        Sortie : (bool) True en cas de contact.
        """
        x_proche, y_proche = self.point_le_plus_proche(brique)
        ecart_x = self.balle.x - x_proche
        ecart_y = self.balle.y - y_proche
        return ecart_x ** 2 + ecart_y ** 2 <= self.balle.rayon ** 2

    def rebondir(self, brique):
        """
        But : faire rebondir la balle sur la face de la brique touchée
        (réflexion de Descartes : inversion de la composante normale).
        Entrée : brique (Brique) : brique touchée.
        Sortie : aucune (modifie la vitesse de la balle).
        """
        x_min, y_min, x_max, y_max = brique.obtenir_boite()
        x_proche, y_proche = self.point_le_plus_proche(brique)
        ecart_x = abs(self.balle.x - x_proche)
        ecart_y = abs(self.balle.y - y_proche)
        if ecart_x == 0 and ecart_y == 0:
            # Centre à l'intérieur : on choisit l'axe de plus faible
            # pénétration.
            penetration_x = min(self.balle.x - x_min, x_max - self.balle.x)
            penetration_y = min(self.balle.y - y_min, y_max - self.balle.y)
            face_laterale = penetration_x < penetration_y
        else:
            face_laterale = ecart_x > ecart_y

        if face_laterale:
            centre_x = (x_min + x_max) / 2
            if self.balle.x < centre_x:
                self.balle.vitesse_x = -abs(self.balle.vitesse_x)
            else:
                self.balle.vitesse_x = abs(self.balle.vitesse_x)
        else:
            centre_y = (y_min + y_max) / 2
            if self.balle.y < centre_y:
                self.balle.vitesse_y = -abs(self.balle.vitesse_y)
            else:
                self.balle.vitesse_y = abs(self.balle.vitesse_y)

    def gerer_collision_briques(self):
        """
        But : traiter la première brique touchée : rebond, coup porté à la
        brique, suppression et points si elle est détruite.
        Entrée : aucune.
        Sortie : (bool) True si une brique a été touchée.
        """
        for brique in self.briques:
            if self.touche(brique):
                self.rebondir(brique)
                if brique.frapper():
                    Explosion(self.canvas, brique)
                    brique.effacer(self.canvas)
                    self.briques.supprimer(brique)
                    self.score += brique.points
                    self.application.afficher_score(self.score)
                else:
                    brique.rafraichir(self.canvas)
                return True
        return False

    def est_gagnee(self):
        """
        But : indiquer si toutes les briques ont été détruites.
        Entrée : aucune.
        Sortie : (bool) True si plus aucune brique.
        """
        return len(self.briques) == 0
