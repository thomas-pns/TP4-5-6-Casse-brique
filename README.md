# TP4-5-6 Casse-brique


**Auteurs :** Thomas CHASSANIS PONS et Camil BOUZIRI

**Dépôt Git :** https://github.com/thomas-pns/TP4-5-6-Casse-brique

## But du programme

Le but de ce TP est de développer notre propre version du jeu classique
Casse-brique (Breakout, 1976), en Python avec le module Tkinter pour
l'interface graphique. Le projet est organisé en classes (programmation
orientée objet) et utilise nos propres structures de données (liste chaînée,
file et pile).

## Lancer le jeu

Le jeu utilise uniquement la bibliothèque standard de Python (Tkinter est
inclus avec Python).

Depuis le dossier du projet, dans l'invite de commandes :

```
python main.py
```

## Règles du jeu

- Cliquer sur **Démarrer** pour lancer une partie.
- Déplacer la raquette avec les **flèches gauche / droite** ou avec la
  **souris**.
- Faire rebondir la balle pour détruire les briques. Chaque brique détruite
  rapporte 10 points.
- Le joueur commence avec **3 vies**. Si la balle tombe en bas de l'écran,
  une vie est perdue et la balle repart du centre.
- À 0 vie, l'écran **Game Over** affiche le score final. On peut relancer une
  partie avec le bouton **Rejouer** ou la touche **Entrée**.
- Les règles sont aussi rappelées dans le menu **Aide > Règles du jeu**.


## Utilisation de l'IA

Nous avons utilisé l'intelligence artificielle pour la partie direction
artistique du jeu :

- l'image de fond (`data/fond.png`), générée par IA ;
- le style néon des briques et de la raquette (couleurs, contours, trame) ;
- la traînée de la balle ;
- l'animation de destruction des briques (éclats) ;
- l'écran Game Over.

## Emplacement des structures de données

Les trois structures demandées sont dans le dossier `structures/` :

| Structure | Fichier | Utilisation dans le jeu |
|---|---|---|
| Liste chaînée | `structures/liste.py` | Stocke les briques du niveau (`creer_grille` dans `jeu/brique.py`, attribut `briques` de `Partie`). |
| File (FIFO) | `structures/file.py` | Stocke les traces de la traînée de la balle : la plus ancienne est retirée en premier (`jeu/balle.py`). |
| Pile (LIFO) | `structures/pile.py` | Implémentée à partir de la liste chaînée. |

La file et la pile sont construites à partir de notre liste chaînée.

## Contenu de l'archive

```
TP4-5-6-Casse-brique/
├── main.py
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   ├── fond.png
│   └── scores.txt
├── jeu/
│   ├── __init__.py
│   ├── application.py
│   ├── partie.py
│   ├── balle.py
│   ├── raquette.py
│   ├── brique.py
│   └── niveau.py
└── structures/
    ├── __init__.py
    ├── liste.py
    ├── file.py
    └── pile.py
```

### Racine

- `main.py` : point d'entrée du programme. Crée l'application et lance la
  boucle principale de Tkinter.
- `README.md` : ce fichier.
- `LICENSE` : licence MIT du projet.
- `.gitignore` : fichiers ignorés par Git (par exemple les dossiers
  `__pycache__`).

### Dossier `jeu/` : le jeu lui-même

- `application.py` : classe `Application`. Gère la fenêtre, le menu, les
  boutons, le fond d'écran, l'affichage du score et des vies, et l'écran
  Game Over avec le bouton Rejouer.
- `partie.py` : classe `Partie`. Contient la boucle de jeu (relancée toutes
  les 20 ms), les collisions de la balle avec la raquette et les briques, la
  perte de vies et la fin de partie.
- `balle.py` : classe `Balle`. Position, vitesse, déplacement, rebonds sur
  les murs et traînée.
- `raquette.py` : classe `Raquette`. Déplacement au clavier et à la souris,
  sans sortir de l'écran.
- `brique.py` : classe de base `Brique`, sous-classe `BriqueNormale`,
  animation `Explosion` et fonction `creer_grille` qui construit le niveau.
  Ce fichier peut aussi être lancé seul pour tester les briques en cliquant
  dessus.
- `niveau.py` : prévu pour la gestion de plusieurs niveaux, pas encore
  implémenté.
- `__init__.py` : fait du dossier un package Python importable.

### Dossier `structures/` : nos structures de données

- `liste.py` : liste simplement chaînée (classes `Noeud` et `Liste`), avec
  ajout en tête et en queue, retrait, suppression et parcours.
- `file.py` : file FIFO (`File`), construite sur la liste chaînée.
- `pile.py` : pile LIFO (`Pile`), construite sur la liste chaînée.
- `__init__.py` : fait du dossier un package Python importable.

### Dossier `data/` : les ressources

- `fond.png` : image de fond du jeu (800 × 600).
- `scores.txt` : prévu pour enregistrer les meilleurs scores, pas encore
  utilisé.