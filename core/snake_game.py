import pygame
import random
import sys
import math

class SnakeGame:
    """Jeu Snake avec ambiance Doom, bordure de feu et lignes de feu létales avec avertissement,
    et mode nuit aléatoire en pixel : en mode nuit, le fond devient noir et seul un éclairage
    pixelisé (5 cellules de rayon) autour du serpent est visible (les bordures sont masquées)."""
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 900
        self.cell_size = 20
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Doom")
        self.clock = pygame.time.Clock()
        self.running = True

        # Mécaniques de feu (définies avant spawn_food)
        self.fire_border_thickness = 1  # en nombre de cases pour la bordure de feu
        self.fire_line_spawn_interval = 10000  # toutes les 10s
        self.fire_line_warning_duration = 200    # 0.2s d'alerte
        self.fire_line_active_duration = 2000    # 2s de ligne létale
        self.last_fire_line_spawn_time = pygame.time.get_ticks()
        self.fire_line = None  # Dictionnaire pour la ligne létale active
        self.fire_line_warning = None  # Dictionnaire pour l'alerte de ligne

        # Mode nuit
        self.night_mode_active = False
        self.last_night_mode_trigger = pygame.time.get_ticks()
        self.night_mode_start_time = 0

        # Score et éléments du jeu
        self.score = 20
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.food = self.spawn_food()
        self.monsters = []
        self.color_monsters = []
        self.max_monsters = 10
        self.spawn_monster()
        self.background_pattern = self.generate_background_pattern()

        # Configuration audio et sons
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        try:
            self.crunch_sound = pygame.mixer.Sound('assets/sounds/crunch_sound.mp3')
        except:
            print("Impossible de charger le son de croc. Vérifiez que le fichier existe.")
            self.crunch_sound = None

        try:
            pygame.mixer.music.load('assets/sounds/snake_game_audio_theme.mp3')
            pygame.mixer.music.set_volume(0.2)  # Régler le volume à 20%
            pygame.mixer.music.play(-1)  # -1 signifie jouer en boucle indéfiniment
        except:
            print("Impossible de charger la musique d'ambiance. Vérifiez que le fichier existe.")

    def generate_background_pattern(self):
        """Génère un motif de fond aléatoire en niveaux de gris pour un effet de pixel art. Chaque cellule est une couleur aléatoire."""
        pattern = []
        for y in range(0, self.screen_height, self.cell_size):
            row = []
            for x in range(0, self.screen_width, self.cell_size):
                grey_value = random.randint(30, 70)
                color = (grey_value, grey_value, grey_value)
                row.append(color)
            pattern.append(row)
        return pattern

    def spawn_food(self):
        """Génère une pomme. Si le score est ≥ 10 (bordure de feu active),
        la pomme apparaît uniquement dans la zone intérieure."""
        if self.score >= 10:
            min_x = self.fire_border_thickness
            max_x = (self.screen_width // self.cell_size) - self.fire_border_thickness - 1
            min_y = self.fire_border_thickness
            max_y = (self.screen_height // self.cell_size) - self.fire_border_thickness - 1
        else:
            min_x = 0
            max_x = (self.screen_width // self.cell_size) - 1
            min_y = 0
            max_y = (self.screen_height // self.cell_size) - 1

        x = random.randint(min_x, max_x) * self.cell_size
        y = random.randint(min_y, max_y) * self.cell_size
        return [x, y]

    def spawn_monster(self):
        """Génère un monstre. Le monstre ne peut pas apparaître sur le serpent, la pomme ou un autre monstre."""
        if len(self.monsters) < self.max_monsters:
            while True:
                x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
                y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
                monster_pos = [x, y]
                if monster_pos not in self.snake and monster_pos != self.food and monster_pos not in self.monsters:
                    self.monsters.append(monster_pos)
                    color = (random.randint(50, 100), 0, random.randint(50, 100))
                    self.color_monsters.append(color)
                    break

    def move_snake(self):
        """Déplace le serpent et gère les collisions avec la pomme et les monstres."""
        head = self.snake[0][:]
        if self.direction == "UP":
            head[1] -= self.cell_size
        elif self.direction == "DOWN":
            head[1] += self.cell_size
        elif self.direction == "LEFT":
            head[0] -= self.cell_size
        elif self.direction == "RIGHT":
            head[0] += self.cell_size
        self.snake.insert(0, head)
        if head == self.food:
            if hasattr(self, 'crunch_sound') and self.crunch_sound:
                self.crunch_sound.play()
            self.food = self.spawn_food()
            self.score += 1
            if self.score % 2 == 0:
                self.spawn_monster()
        else:
            self.snake.pop()

    def move_monsters(self):
        """Déplace les monstres vers la tête du serpent."""
        snake_head = self.snake[0]
        updated_monsters = []
        for monster in self.monsters:
            dx = snake_head[0] - monster[0]
            dy = snake_head[1] - monster[1]
            monster_move = monster[:]
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
            if (0 <= monster_move[0] < self.screen_width and 0 <= monster_move[1] < self.screen_height):
                updated_monsters.append(monster_move)
            else:
                updated_monsters.append(monster)
        self.monsters = updated_monsters

    def update_fire_line(self):
        """Gère le cycle de la ligne de feu dès le score 20.
        D'abord 0.2s d'alerte clignotante, puis la ligne apparaît pendant 2s."""
        if self.score >= 20:
            current_time = pygame.time.get_ticks()
            if self.fire_line is None and self.fire_line_warning is None and \
               (current_time - self.last_fire_line_spawn_time >= self.fire_line_spawn_interval - self.fire_line_warning_duration):
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    min_row = self.fire_border_thickness
                    max_row = (self.screen_height // self.cell_size) - self.fire_border_thickness - 1
                    pos = random.randint(min_row, max_row) * self.cell_size
                else:
                    min_col = self.fire_border_thickness
                    max_col = (self.screen_width // self.cell_size) - self.fire_border_thickness - 1
                    pos = random.randint(min_col, max_col) * self.cell_size
                self.fire_line_warning = {"orientation": orientation, "pos": pos, "warning_start": current_time}
            if self.fire_line_warning is not None and (current_time - self.fire_line_warning["warning_start"] >= self.fire_line_warning_duration):
                self.fire_line = {"orientation": self.fire_line_warning["orientation"],
                                   "pos": self.fire_line_warning["pos"],
                                   "spawn_time": current_time}
                self.fire_line_warning = None
            if self.fire_line is not None and (current_time - self.fire_line["spawn_time"] >= self.fire_line_active_duration):
                self.fire_line = None
                self.last_fire_line_spawn_time = current_time

    def update_night_mode(self):
        """Active le mode nuit toutes les 15s pour 5s."""
        current_time = pygame.time.get_ticks()
        if not self.night_mode_active and (current_time - self.last_night_mode_trigger >= 15000):
            self.night_mode_active = True
            self.night_mode_start_time = current_time
            print("Mode nuit activé")  # Debug
        if self.night_mode_active and (current_time - self.night_mode_start_time >= 5000):
            self.night_mode_active = False
            self.last_night_mode_trigger = current_time
            print("Mode nuit désactivé")  # Debug

    def check_collision(self):
        """Vérifie les collisions avec les bords, le serpent, les monstres et la bordure de feu."""
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.screen_width or head[1] < 0 or head[1] >= self.screen_height:
            return True
        if head in self.snake[1:]:
            return True
        if head in self.monsters:
            return True
        # En mode jour, la bordure de feu s'affiche dès le score 10
        if not self.night_mode_active and self.score >= 10:
            border = self.fire_border_thickness * self.cell_size
            if (head[0] < border or head[0] >= self.screen_width - border or
                head[1] < border or head[1] >= self.screen_height - border):
                return True
        if self.score >= 20 and self.fire_line is not None:
            if self.fire_line["orientation"] == "horizontal":
                if head[1] >= self.fire_line["pos"] and head[1] < self.fire_line["pos"] + self.cell_size:
                    return True
            else:
                if head[0] >= self.fire_line["pos"] and head[0] < self.fire_line["pos"] + self.cell_size:
                    return True
        return False

    def draw_snake(self):
        """Dessine le serpent avec une couleur rouge foncée pour la tête et rouge clair pour le reste."""
        for i, segment in enumerate(self.snake):
            red_value = max(255 - (i * 20), 100)
            color = (red_value, 0, 0)
            pygame.draw.rect(self.screen, color, (*segment, self.cell_size, self.cell_size))

    def draw_fire_border(self):
        """Dessine la bordure de feu (uniquement en mode jour)."""
        flame_colors = [
            (255, 0, 0), (255, 69, 0), (255, 140, 0),
            (255, 165, 0), (255, 215, 0)
        ]
        for i in range(self.fire_border_thickness):
            for x in range(0, self.screen_width, self.cell_size):
                color = random.choice(flame_colors)
                y = i * self.cell_size
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
            for x in range(0, self.screen_width, self.cell_size):
                color = random.choice(flame_colors)
                y = self.screen_height - (i+1) * self.cell_size
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
            for y in range(0, self.screen_height, self.cell_size):
                color = random.choice(flame_colors)
                x = i * self.cell_size
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
            for y in range(0, self.screen_height, self.cell_size):
                color = random.choice(flame_colors)
                x = self.screen_width - (i+1) * self.cell_size
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def draw_fire_line(self):
        """Dessine la ligne de feu létale."""
        if self.fire_line is None:
            return
        flame_colors = [
            (255, 0, 0), (255, 69, 0), (255, 140, 0),
            (255, 165, 0), (255, 215, 0)
        ]
        color = random.choice(flame_colors)
        if self.fire_line["orientation"] == "horizontal":
            y = self.fire_line["pos"]
            pygame.draw.rect(self.screen, color, (0, y, self.screen_width, self.cell_size))
        else:
            x = self.fire_line["pos"]
            pygame.draw.rect(self.screen, color, (x, 0, self.cell_size, self.screen_height))

    def draw_fire_line_warning(self):
        """Dessine l'alerte de ligne de feu."""
        if self.fire_line_warning is None:
            return
        current_time = pygame.time.get_ticks()
        if (current_time // 100) % 2 == 0:
            warning_color = (255, 255, 255)
            if self.fire_line_warning["orientation"] == "horizontal":
                y = self.fire_line_warning["pos"]
                pygame.draw.rect(self.screen, warning_color, (0, y, self.screen_width, self.cell_size))
            else:
                x = self.fire_line_warning["pos"]
                pygame.draw.rect(self.screen, warning_color, (x, 0, self.cell_size, self.screen_height))

    def draw_night_overlay_pixel(self):
        """
        Crée un overlay pixelisé : l'écran est divisé en cellules.
        Chaque cellule reçoit une opacité en fonction de sa distance (discrétisée)
        par rapport à la tête du serpent (centre de lumière).
        Les cellules proches (< 3 cases) sont transparentes,
        puis l'opacité augmente jusqu'à 255 au-delà de 5 cases.
        """
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        head_center = (self.snake[0][0] + self.cell_size // 2, self.snake[0][1] + self.cell_size // 2)
        for y in range(0, self.screen_height, self.cell_size):
            for x in range(0, self.screen_width, self.cell_size):
                cell_center = (x + self.cell_size // 2, y + self.cell_size // 2)
                d = math.hypot(cell_center[0] - head_center[0], cell_center[1] - head_center[1])
                if d < 3 * self.cell_size:
                    alpha = 0
                elif d < 4 * self.cell_size:
                    alpha = 128
                elif d < 5 * self.cell_size:
                    alpha = 200
                else:
                    alpha = 255
                overlay.fill((0, 0, 0, alpha), rect=pygame.Rect(x, y, self.cell_size, self.cell_size))
        self.screen.blit(overlay, (0, 0))

    def draw_elements(self):
        """Dessine les éléments du jeu : fond, serpent, pomme, monstres, bordure de feu, ligne de feu."""
        # Dessiner le fond en mode pixel
        for y, row in enumerate(self.background_pattern):
            for x, color in enumerate(row):
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        self.draw_snake()
        pygame.draw.rect(self.screen, (255, 215, 0), (*self.food, self.cell_size, self.cell_size))
        pygame.draw.rect(self.screen, (0, 0, 0), (*self.food, self.cell_size, self.cell_size), 1)
        for monster, color in zip(self.monsters, self.color_monsters):
            pygame.draw.rect(self.screen, color, (*monster, self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, (0, 0, 0), (*monster, self.cell_size, self.cell_size), 1)
        # En mode jour, afficher la bordure de feu
        if not self.night_mode_active and self.score >= 10:
            self.draw_fire_border()
        if self.score >= 20:
            if self.fire_line_warning is not None:
                self.draw_fire_line_warning()
            elif self.fire_line is not None:
                self.draw_fire_line()
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        # Ne pas appeler flip() ici

    def run(self):
        """Boucle principale du jeu."""
        monster_move_timer = 0
        monster_move_interval = 10
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
            self.move_snake()
            monster_move_timer += 1
            if monster_move_timer % monster_move_interval == 0:
                self.move_monsters()
            self.update_fire_line()
            self.update_night_mode()
            if self.check_collision():
                print(f"Game Over! Your score: {self.score}")
                self.running = False
            self.draw_elements()
            # Si mode nuit, dessiner l'overlay pixelisé par-dessus
            if self.night_mode_active:
                self.draw_night_overlay_pixel()
            pygame.display.flip()
            self.clock.tick(10)
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.run()
