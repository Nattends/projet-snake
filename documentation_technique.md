# Documentation Technique

## Architecture Globale

Le jeu Snake est développé en Python en utilisant la bibliothèque Pygame. L'architecture du projet est organisée de manière modulaire avec une séparation claire des responsabilités entre les différentes classes et modules.

### Structure des Dossiers

```
projet-snake/
├── assets/
│   ├── images/
│   │   └── menu/
│   └── sounds/
├── core/
│   ├── __init__.py
│   ├── menu.py
│   ├── options_page.py
│   ├── score_page.py
│   └── snake_game.py
├── data/
├── docs/
├── tests/
│   └── test_snake_game.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── main.py
└── requirements.txt
```

## Composants Principaux

### 1. Module `main.py`

Point d'entrée de l'application qui initialise Pygame et lance le menu principal.

### 2. Module `core`

#### 2.1 `menu.py`

La classe `Menu` gère l'affichage et les interactions du menu principal. Elle permet de naviguer vers les différentes sections du jeu (jouer, scores, options).

#### 2.2 `snake_game.py`

La classe `SnakeGame` est le cœur du jeu, elle gère :
- Le mouvement du serpent
- La génération de nourriture
- La détection des collisions
- Les mécaniques spéciales comme la bordure de feu et le mode nuit
- Les monstres qui poursuivent le serpent
- Les effets sonores et la musique d'ambiance

#### 2.3 `score_page.py`

La classe `ScorePage` affiche les scores enregistrés des parties précédentes.

#### 2.4 `options_page.py`

La classe `OptionsPage` permet de configurer certains paramètres du jeu.

### 3. Module `utils`

#### 3.1 `helpers.py`

Contient des fonctions utilitaires comme `resize_image` pour le redimensionnement d'images.

## Détails d'Implémentation

### Système de Son

Le jeu implémente deux types de systèmes sonores :

1. **Effets sonores ponctuels** : Utilisation de `pygame.mixer.Sound`
   ```python
   self.crunch_sound = pygame.mixer.Sound('assets/sounds/crunch.wav')
   self.crunch_sound.play()  # Joué lorsque le serpent mange une nourriture
   ```

2. **Musique d'ambiance en boucle** : Utilisation de `pygame.mixer.music`
   ```python
   pygame.mixer.music.load('assets/sounds/ambient_music.mp3')
   pygame.mixer.music.set_volume(0.5)  # Volume à 50%
   pygame.mixer.music.play(-1)  # -1 signifie jouer en boucle indéfiniment
   ```

### Mécaniques de Jeu Spéciales

#### Bordure de Feu
- Apparaît à partir d'un score de 10
- Rend les bords de l'écran mortels
- Implémentée dans la méthode `draw_fire_border()`

#### Mode Nuit
- Active aléatoirement toutes les 15 secondes pendant 5 secondes
- Limite la visibilité autour du serpent avec un effet de lumière pixelisé
- Implémenté dans les méthodes `update_night_mode()` et `draw_night_overlay_pixel()`

#### Lignes de Feu
- Apparaissent à partir d'un score de 20
- Une alerte visuelle précède l'apparition d'une ligne mortelle
- Implémentées dans les méthodes `update_fire_line()`, `draw_fire_line_warning()` et `draw_fire_line()`

#### Monstres
- Poursuivent le serpent
- Apparaissent progressivement avec l'augmentation du score
- Implémentés dans les méthodes `spawn_monster()` et `move_monsters()`

### Système de Collision

La détection des collisions est gérée par la méthode `check_collision()` qui vérifie :
- Les collisions avec les bords de l'écran
- Les collisions avec le corps du serpent
- Les collisions avec les monstres
- Les collisions avec la bordure de feu (si active)
- Les collisions avec les lignes de feu (si actives)

### Gestion des Scores

Les scores sont sauvegardés dans un fichier JSON et peuvent être consultés dans la page des scores. Le score augmente à chaque fois que le serpent mange une nourriture.

## Algorithmes Clés

### Mouvement du Serpent

```python
def move_snake(self):
    head = self.snake[0][:]  # Copie de la tête actuelle
    
    # Calcul de la nouvelle position de la tête selon la direction
    if self.direction == "UP":
        head[1] -= self.cell_size
    elif self.direction == "DOWN":
        head[1] += self.cell_size
    elif self.direction == "LEFT":
        head[0] -= self.cell_size
    elif self.direction == "RIGHT":
        head[0] += self.cell_size
        
    # Insertion de la nouvelle tête en position 0
    self.snake.insert(0, head)
    
    # Si la tête touche la nourriture
    if head == self.food:
        # Jouer le son
        if hasattr(self, 'crunch_sound') and self.crunch_sound:
            self.crunch_sound.play()
            
        # Générer une nouvelle nourriture et augmenter le score
        self.food = self.spawn_food()
        self.score += 1
        
        # Spawn de monstre tous les 2 points
        if self.score % 2 == 0:
            self.spawn_monster()
    else:
        # Si pas de nourriture mangée, on retire le dernier segment
        self.snake.pop()
```

### Mouvement des Monstres

Les monstres se déplacent intelligemment vers le serpent en calculant la direction la plus efficace :

```python
def move_monsters(self):
    snake_head = self.snake[0]
    updated_monsters = []
    for monster in self.monsters:
        dx = snake_head[0] - monster[0]
        dy = snake_head[1] - monster[1]
        monster_move = monster[:]
        
        # Prioriser le mouvement selon l'axe avec la plus grande distance
        if abs(dx) > abs(dy):
            if dx > 0:
                monster_move[0] += self.cell_size
            elif dx < 0:
                monster_move[0] -= self.cell_size
        else:
            if dy > 0:
                monster_move[1] += self.cell_size
            elif dy < 0:
                monster_move[1] -= self.cell_size
                
        # Vérifier que le monstre reste dans les limites
        if (0 <= monster_move[0] < self.screen_width and 
            0 <= monster_move[1] < self.screen_height):
            updated_monsters.append(monster_move)
        else:
            updated_monsters.append(monster)
            
    self.monsters = updated_monsters
```

## Documentation du code

La documentation technique du projet Snake se trouve dans le dossier `docs`. Cette documentation est générée à l'aide de Sphinx.

Pour consulter la documentation, veuillez naviguer vers le dossier `docs` et ouvrir le fichier `index.html` dans votre navigateur.

```bash
cd docs
open index.html
```

Assurez-vous d'avoir généré la documentation en utilisant Sphinx avant de tenter de l'ouvrir.

```bash
cd docs
make html
```

Pour plus d'informations sur Sphinx, veuillez consulter la [documentation officielle de Sphinx](https://www.sphinx-doc.org/).