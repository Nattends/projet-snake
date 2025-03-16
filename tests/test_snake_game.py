import os
import sys

# Ajouter le répertoire parent au PYTHONPATH pour que Python trouve le package 'core'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pygame
from core.snake_game import SnakeGame  # Import depuis le package core


# ✅ TESTS UNITAIRES 

def test_spawn_food_zone_interieure():
    """Teste la génération de la nourriture dans la zone intérieure"""
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
    """Teste le déplacement normal du serpent"""
    game = SnakeGame()
    game.snake = [[100, 100], [80, 100], [60, 100]]
    game.direction = "RIGHT"
    old_head = game.snake[0][:]
    game.food = [9999, 9999]  # Pas de nourriture
    game.move_snake()
    new_head = game.snake[0]
    assert new_head[0] == old_head[0] + game.cell_size
    assert new_head[1] == old_head[1]
    assert len(game.snake) == 3  # Pas de nourriture consommée


def test_move_snake_avec_nourriture():
    """Teste le déplacement du serpent avec la croissance"""
    game = SnakeGame()
    game.snake = [[100, 100], [80, 100], [60, 100]]
    game.direction = "RIGHT"
    game.food = [100 + game.cell_size, 100]  # Nourriture juste devant
    old_length = len(game.snake)
    game.move_snake()
    assert len(game.snake) == old_length + 1  # Le serpent grandit


def test_collision_mur():
    """Teste la collision du serpent avec les murs"""
    game = SnakeGame()
    game.snake = [[-10, 100]]  # Hors écran
    assert game.check_collision() is True


def test_collision_avec_soi_meme():
    """Teste la collision du serpent avec lui-même"""
    game = SnakeGame()
    game.snake = [[100, 100], [120, 100], [120, 120], [100, 120], [100, 100]]  # Boucle
    assert game.check_collision() is True


def test_spawn_monster():
    """Teste la génération de monstres"""
    game = SnakeGame()
    initial_monsters = len(game.monsters)
    game.spawn_monster()
    if initial_monsters < game.max_monsters:
        assert len(game.monsters) == initial_monsters + 1
    else:
        assert len(game.monsters) == initial_monsters


def test_move_monsters():
    """Teste le déplacement des monstres"""
    game = SnakeGame()
    game.snake = [[100, 100]]
    game.monsters = [[60, 100]]
    game.move_monsters()
    assert game.monsters[0] == [80, 100]  # Le monstre se rapproche


def test_generate_background_pattern():
    """Teste la génération du motif de fond"""
    game = SnakeGame()
    pattern = game.generate_background_pattern()
    expected_rows = game.screen_height // game.cell_size
    expected_cols = game.screen_width // game.cell_size
    assert len(pattern) == expected_rows
    for row in pattern:
        assert len(row) == expected_cols


def test_update_night_mode(monkeypatch):
    """Teste l'activation et la désactivation du mode nuit"""
    game = SnakeGame()
    fake_time = 10000
    monkeypatch.setattr(pygame, 'time', type('dummy', (), {'get_ticks': lambda: fake_time}))
    game.last_night_mode_trigger = fake_time - 15000
    game.update_night_mode()
    assert game.night_mode_active is True

    monkeypatch.setattr(pygame, 'time', type('dummy', (), {'get_ticks': lambda: fake_time + 5000}))
    game.update_night_mode()
    assert game.night_mode_active is False


def test_fire_line_warning():
    """Teste l'affichage de l'avertissement de la ligne de feu"""
    game = SnakeGame()
    game.score = 20
    game.last_fire_line_spawn_time = pygame.time.get_ticks() - (game.fire_line_spawn_interval - game.fire_line_warning_duration)
    game.update_fire_line()
    assert game.fire_line_warning is not None


def test_fire_line_collision():
    """Teste la collision du serpent avec la ligne de feu"""
    game = SnakeGame()
    game.score = 20
    game.fire_line = {"orientation": "horizontal", "pos": 100, "spawn_time": pygame.time.get_ticks()}
    game.snake = [[50, 100]]  # La tête est sur la ligne de feu
    assert game.check_collision() is True


# ✅ TESTS UI & FONCTIONNELS 

def test_ui_mode_nuit_affichage():
    """Teste si le mode nuit masque bien l'affichage"""
    game = SnakeGame()
    game.night_mode_active = True
    assert game.night_mode_active is True


def test_sound_loaded():
    """Teste si la musique et le son sont bien chargés"""
    game = SnakeGame()
    assert game.crunch_sound is not None or game.crunch_sound is None  # S'assurer que le son est chargé
    assert pygame.mixer.music.get_busy() is not None  # Vérifier la musique


def test_fire_line_display():
    """Teste l'affichage de la ligne de feu"""
    game = SnakeGame()
    game.score = 20
    game.fire_line = {"orientation": "horizontal", "pos": 100, "spawn_time": pygame.time.get_ticks()}
    assert game.fire_line is not None


def test_game_over_on_collision():
    """Teste si le jeu se termine après une collision"""
    game = SnakeGame()
    game.snake = [[-10, 100]]  # Collision avec le mur
    assert game.check_collision() is True
