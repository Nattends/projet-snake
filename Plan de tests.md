# 📜 Plan de Tests - Snake Doom

## 1️⃣ Objectifs du Test
- Vérifier les fonctionnalités principales du jeu : déplacement du serpent, nourriture, monstres, bordures de feu, mode nuit et lignes de feu létales.
- Tester la détection des collisions (murs, soi-même, monstres, ligne de feu).
- Vérifier l’affichage du mode nuit et la gestion des lignes de feu.
- Tester la gestion des sons (musique et effets sonores).
- S'assurer que les événements critiques (Game Over) se produisent correctement.

---

## 2️⃣ Cas de Tests et Scénarios

### 🟢 **Tests Unitaires**
| ID | Test | Entrée | Résultat attendu |
|----|------|--------|------------------|
| **TU-01** | Génération de nourriture dans la zone intérieure | Score ≥ 10 | La nourriture apparaît dans la zone intérieure sans toucher la bordure de feu. |
| **TU-02** | Déplacement normal du serpent | Direction `RIGHT` | La tête du serpent avance d’une cellule vers la droite, la longueur reste inchangée. |
| **TU-03** | Déplacement du serpent avec consommation de nourriture | Nourriture devant la tête | Le serpent grandit et la nourriture est repositionnée. |
| **TU-04** | Collision avec un mur | Tête hors écran | La partie se termine. |
| **TU-05** | Collision avec soi-même | Tête du serpent touche son propre corps | La partie se termine. |
| **TU-06** | Génération d’un monstre | Avant génération | Un monstre apparaît sur une case libre. |
| **TU-07** | Déplacement des monstres | Monstre à gauche du serpent | Le monstre se rapproche du serpent. |
| **TU-08** | Génération du fond pixelisé | Le jeu démarre | Un fond aléatoire en niveaux de gris est affiché. |
| **TU-09** | Activation du mode nuit | Temps écoulé de 15s | Le mode nuit s’active pour 5s. |
| **TU-10** | Désactivation du mode nuit | 5s après activation | Le mode nuit se désactive. |
| **TU-11** | Avertissement ligne de feu | Score ≥ 20 | Une alerte est affichée avant l’apparition de la ligne de feu. |
| **TU-12** | Collision avec la ligne de feu | Serpent sur la ligne de feu | La partie se termine. |

---

### 🟡 **Tests Fonctionnels**
| ID | Test | Scénario | Résultat attendu |
|----|------|----------|------------------|
| **TF-01** | Mode nuit activé | Mode nuit activé manuellement | Le mode nuit est bien actif. |
| **TF-02** | Chargement du son | Le jeu démarre | La musique et les effets sonores sont bien chargés. |
| **TF-03** | Affichage de la ligne de feu | La ligne de feu apparaît | La ligne de feu est correctement affichée. |
| **TF-04** | Fin de partie en cas de collision | Serpent touche un mur | La partie se termine. |

---

## 3️⃣ Outils et automatisation
- **pytest** : Exécution des tests unitaires et fonctionnels.
- **Mocking avec `monkeypatch`** : Simuler le temps (`pygame.time.get_ticks()`) et autres dépendances.

---

## 4️⃣ Répartition des Tests
- **Développeur** : Tests unitaires (TU-01 à TU-12).
- **Testeur** : Tests fonctionnels (TF-01 à TF-04).

---

## 5️⃣ Conclusion

Les tests unitaires et fonctionnels permettent de garantir le bon fonctionnement du jeu Snake Doom. Les tests automatisés assurent une vérification continue des fonctionnalités et une détection rapide des anomalies. Les cas de tests couvrent les scénarios critiques et les fonctionnalités principales du jeu.

---
