# Header
# -*- coding: utf-8 -*-
"""
Objectifs du fichier :
    Orchestrer la boucle de jeu, détecter collisions (balle/raquette, balle/briques, balle/murs), gérer fin de partie (victoire/défaite).

Par :
    Thomas CHASSANIS PONS et Camil BOUZIRI

Réalisé le 06/10/2026

ToDo List:
    Power-ups, niveaux multiples, système de combo, sauvegarde/reprise partie.
"""

class Partie:
    def __init__(self, application, canvas, balle, raquette, brique, score):
<<<<<<< HEAD
        self.application = application
    def __init__(self, application, canvas, balle, raquette, brique, score):
=======
>>>>>>> 9a36c13 (merge vers main perte de vie)
        self.application = application
        self.canvas = canvas
        self.balle = balle
        self.raquette = raquette
        self.brique = brique
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
        x1,y1,x2,y2 = coords_balle
        rx1,ry1,rx2,ry2 = coords_raquette

        if x1 <= rx2 and x2 >= rx1 and y2 >= ry1 and y1 <= ry2:
            self.balle.vitesse_y = -self.balle.vitesse_y
            print("Collision détectée !")

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

        self.application.fenetre.after(20, self.boucle_jeu)

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
            # Centre à l'intérieur : on choisit l'axe de plus faible pénétration.
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
        But : traiter la première brique touchée : rebond, perte de vie,
        suppression et points si elle est détruite.
        Entrée : aucune.
        Sortie : (bool) True si une brique a été touchée.
        """
        for brique in self.briques:
            if self.touche(brique):
                self.rebondir(brique)
                if brique.frapper():
                    brique.effacer(self.canvas)
                    self.briques.supprimer(brique)
                    self.score += brique.points
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