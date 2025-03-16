# Cahier des Charges : Développement d’un Jeu Snake en Python

## 1. Introduction
Le projet consiste à développer un jeu **Snake** en utilisant Python. Le jeu sera conçu pour une expérience utilisateur simple et interactive, avec des fonctionnalités de base et éventuellement des options avancées. Ce document décrit les spécifications fonctionnelles et techniques du jeu.

---

## 2. Objectifs
- Créer un jeu Snake fonctionnel.
- Offrir une interface utilisateur intuitive et agréable.
- Assurer un gameplay fluide et sans bugs.
- Implémenter des fonctionnalités pour rendre le jeu captivant (e.g., niveaux de difficulté, score).

---

## 3. Fonctionnalités

- **Déplacement du serpent** :
  - Le serpent doit se déplacer dans quatre directions : haut, bas, gauche, droite.
  - Les contrôles sont effectués via le clavier (flèches directionnelles).

- **Alimentation du serpent** :
  - Un objet (la "nourriture") apparaît aléatoirement sur l'écran.
  - Lorsque le serpent mange la nourriture, sa taille augmente.

- **Gestion des collisions** :
  - Collision avec les bords de l’écran : entraîne la fin de la partie.
  - Collision avec le corps du serpent : entraîne la fin de la partie.

- **Apparition de monstres** :
  - Des obstacles (monstres) apparaissent aléatoirement sur l'écran.
  - Les monstres suivent le serpent.
  - Si le serpent entre en collision avec un monstre, la partie est terminée.

- **Apparition de lignes de feu** :
  - Des lignes de feu apparaissent aléatoirement sur l'écran.
  - Si le serpent entre en collision avec une ligne de feu, la partie est terminée.

- **Mode nuit aléatoire** :
  - Ce malus restreint la vision du joueur à quelque pixels autour du serpent.
  - Le mode nuit est activé aléatoirement.

- **Système de score** :
  - Un score est affiché et augmente à chaque fois que le serpent mange une nourriture.

- **Sauvegarde du score** :
  - Stocker les meilleurs scores dans un fichier.

- **Effets visuels et sonores** :
  - Animation ou sons pour les actions importantes (manger un fruit).
  - Musique de fond.

---

## 4. Contraintes Techniques
- **Langage** : Python.
- **Bibliothèques** :
  - Utilisation de `pygame` pour la gestion des graphiques et des événements.
- **Compatibilité** :
  - Le jeu doit fonctionner sur les principales plateformes (Windows, macOS, Linux).
- **Structure du Code** :
  - Respect des bonnes pratiques de programmation (modularité, documentation, commentaires).

---

## 5. Interface Utilisateur
- **Écran principal** :
  - Boutons : Jouer, Scores, Paramètres.
- **Écran de jeu** :
  - Zone de jeu de taille prédéfinie.
- ** Fin de partie** :
  - Lorsque le joueur perd, la fenêtre se ferme.
  - Son score est enregistré et consultable dans le menu Scores.

---

## 6. Scénarios d'Utilisation
1. **Lancement du jeu** :
   - L’utilisateur démarre le jeu depuis un menu principal.
2. **Déroulement d’une partie** :
   - Le serpent se déplace, mange des nourritures et évite les collisions.
   - Le score augmente en fonction des actions.
3. **Fin de la partie** :
   - Si une collision est détectée, la partie se termine.

---

## 7. Livrables
1. Code source complet du jeu.
2. Documentation technique.
3. Fichier de sauvegarde des scores.
4. Assets graphiques ou sonores.

---

## 8. Ressources Nécessaires
- Environnement de développement Python installé (e.g., PyCharm, VSCode).
- Bibliothèque `pygame` installée.
- Graphiques simples pour le serpent, la nourriture et le fond d’écran.

