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
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, self.cell_size, self.cell_size))
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, self.cell_size, self.cell_size))
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

