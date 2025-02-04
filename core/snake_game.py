import pygame
import random
import sys
import json

class SnakeGame:
    """Classe pour la logique du jeu Snake"""
    def __init__(self, background_img):
        self.screen_width = 500
        self.screen_height = 500
        self.cell_size = 20
        self.background_img = pygame.transform.scale(background_img, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake II")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.food = self.spawn_food()
        self.score = 0

        # Chargement des sprites
        self.sprites = {
            "head_up": pygame.image.load("assets/sprites/head_up.png"),
            "head_down": pygame.image.load("assets/sprites/head_down.png"),
            "head_left": pygame.image.load("assets/sprites/head_left.png"),
            "head_right": pygame.image.load("assets/sprites/head_right.png"),
            "body_horizontal": pygame.image.load("assets/sprites/body_horizontal.png"),
            "body_vertical": pygame.image.load("assets/sprites/body_vertical.png"),
            "body_topleft": pygame.image.load("assets/sprites/body_topleft.png"),
            "body_topright": pygame.image.load("assets/sprites/body_topright.png"),
            "body_bottomleft": pygame.image.load("assets/sprites/body_bottomleft.png"),
            "body_bottomright": pygame.image.load("assets/sprites/body_bottomright.png"),
            "tail_up": pygame.image.load("assets/sprites/tail_up.png"),
            "tail_down": pygame.image.load("assets/sprites/tail_down.png"),
            "tail_left": pygame.image.load("assets/sprites/tail_left.png"),
            "tail_right": pygame.image.load("assets/sprites/tail_right.png"),
            "apple": pygame.image.load("assets/sprites/apple.png")
        }

        # Agrandir la pomme (changer la taille de l'image)
        self.sprites["apple"] = pygame.transform.scale(self.sprites["apple"], (self.cell_size * 2, self.cell_size * 2))

    def spawn_food(self):
        x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
        y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
        return [x, y]

    def move_snake(self):
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
            self.food = self.spawn_food()
            self.score += 1
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.screen_width or head[1] < 0 or head[1] >= self.screen_height:
            return True
        if head in self.snake[1:]:
            return True
        return False

    def draw_elements(self):
        self.screen.blit(self.background_img, (0, 0))

        # Dessiner la pomme
        self.screen.blit(self.sprites["apple"], tuple(self.food))

        # Dessiner le serpent
        for i, segment in enumerate(self.snake):
            if i == 0:  # Tête
                if self.direction == "UP":
                    img = self.sprites["head_up"]
                elif self.direction == "DOWN":
                    img = self.sprites["head_down"]
                elif self.direction == "LEFT":
                    img = self.sprites["head_left"]
                else:
                    img = self.sprites["head_right"]
            elif i == len(self.snake) - 1:  # Queue
                prev = self.snake[i - 1]
                if prev[0] < segment[0]:
                    img = self.sprites["tail_right"]
                elif prev[0] > segment[0]:
                    img = self.sprites["tail_left"]
                elif prev[1] < segment[1]:
                    img = self.sprites["tail_down"]
                else:
                    img = self.sprites["tail_up"]
            else:  # Corps
                prev = self.snake[i - 1]
                next_seg = self.snake[i + 1]

                if prev[0] == next_seg[0]:  # Vertical
                    img = self.sprites["body_vertical"]
                elif prev[1] == next_seg[1]:  # Horizontal
                    img = self.sprites["body_horizontal"]
                else:  # Coin
                    if (prev[0] < segment[0] and next_seg[1] < segment[1]) or (next_seg[0] < segment[0] and prev[1] < segment[1]):
                        img = self.sprites["body_topleft"]
                    elif (prev[0] > segment[0] and next_seg[1] < segment[1]) or (next_seg[0] > segment[0] and prev[1] < segment[1]):
                        img = self.sprites["body_topright"]
                    elif (prev[0] < segment[0] and next_seg[1] > segment[1]) or (next_seg[0] < segment[0] and prev[1] > segment[1]):
                        img = self.sprites["body_bottomleft"]
                    else:
                        img = self.sprites["body_bottomright"]

            self.screen.blit(img, tuple(segment))
        pygame.display.flip()

    def save_score(self):
        try:
            with open("data/scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        scores.append(self.score)

        with open("data/scores.json", "w") as file:
            json.dump(scores, file)

    def run(self):
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
            if self.check_collision():
                self.save_score()
                print(f"Game Over! Your score: {self.score}")
                self.running = False
            self.draw_elements()
            self.clock.tick(10)
        pygame.quit()
        sys.exit()
