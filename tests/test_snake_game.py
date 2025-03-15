import os
import sys

# Ajouter le répertoire parent au PYTHONPATH pour que Python trouve le package 'core'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pygame
from core.snake_game import SnakeGame  # Import depuis le package core

def test_spawn_food_zone_interieure():
    game = SnakeGame()
    game.score = 10  # Active la restriction de la bordure de feu
    food = game.spawn_food()
    # Calculer les bornes internes autorisées pour la pomme
    min_cell = game.fire_border_thickness
    max_cell_x = (game.screen_width // game.cell_size) - game.fire_border_thickness - 1
    max_cell_y = (game.screen_height // game.cell_size) - game.fire_border_thickness - 1
    x_cell = food[0] // game.cell_size
    y_cell = food[1] // game.cell_size
    assert min_cell <= x_cell <= max_cell_x
    assert min_cell <= y_cell <= max_cell_y

def test_move_snake_normal():
    game = SnakeGame()
    # Initialiser le serpent avec trois segments
    game.snake = [[100, 100], [80, 100], [60, 100]]
    game.direction = "RIGHT"
    old_head = game.snake[0][:]
    # Positionner la nourriture hors de portée pour éviter la croissance
    game.food = [9999, 9999]
    game.move_snake()
    new_head = game.snake[0]
    # La tête doit se déplacer d'une cellule vers la droite
    assert new_head[0] == old_head[0] + game.cell_size
    assert new_head[1] == old_head[1]
    # La longueur doit rester identique (puisque la nourriture n'est pas mangée)
    assert len(game.snake) == 3

def test_move_snake_avec_nourriture():
    game = SnakeGame()
    game.snake = [[100, 100], [80, 100], [60, 100]]
    game.direction = "RIGHT"
    # Placer la nourriture juste devant la tête pour provoquer la croissance
    game.food = [100 + game.cell_size, 100]
    old_length = len(game.snake)
    game.move_snake()
    # Le serpent s'allonge : la longueur doit augmenter de 1
    assert len(game.snake) == old_length + 1

def test_collision_mur():
    game = SnakeGame()
    # Positionner la tête du serpent en dehors des limites de l'écran
    game.snake = [[-10, 100]] + game.snake[1:]
    assert game.check_collision() is True

def test_spawn_monster():
    game = SnakeGame()
    initial_monsters = len(game.monsters)
    game.spawn_monster()
    # Vérifier que le nombre de monstres augmente s'il est inférieur au maximum autorisé
    if initial_monsters < game.max_monsters:
        assert len(game.monsters) == initial_monsters + 1
    else:
        assert len(game.monsters) == initial_monsters

def test_generate_background_pattern():
    game = SnakeGame()
    pattern = game.generate_background_pattern()
    expected_rows = game.screen_height // game.cell_size
    expected_cols = game.screen_width // game.cell_size
    assert len(pattern) == expected_rows
    for row in pattern:
        assert len(row) == expected_cols

def test_update_night_mode(monkeypatch):
    game = SnakeGame()
    # Simuler un temps de départ
    fake_time = 10000
    # Remplacer pygame.time.get_ticks() pour contrôler l'écoulement du temps
    monkeypatch.setattr(pygame, 'time', type('dummy', (), {'get_ticks': lambda: fake_time}))
    game.last_night_mode_trigger = fake_time - 15000  # Conditions pour activer le mode nuit
    game.update_night_mode()
    assert game.night_mode_active is True

    # Simuler 5 secondes plus tard pour désactiver le mode nuit
    monkeypatch.setattr(pygame, 'time', type('dummy', (), {'get_ticks': lambda: fake_time + 5000}))
    game.update_night_mode()
    assert game.night_mode_active is False
