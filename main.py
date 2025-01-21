import pygame
import sys
import random
import json


def resize_image(image, desired_height):
    """Redimensionner une image en fonction de la hauteur désirée"""
    height = image.get_height()
    width = image.get_width()
    ratio = width / height
    new_width = int(desired_height * ratio)
    return pygame.transform.scale(image, (new_width, desired_height))


class Menu:
    """Classe représentant le menu principal"""
    def __init__(self, background_img):
        self.screen_width = 500
        self.screen_height = 900
        self.background_img = background_img
        self.logo_img = resize_image(pygame.image.load('./assets/images/menu/logo.png'), 80)
        self.jouer_img = resize_image(pygame.image.load('./assets/images/menu/jouer.png'), 50)
        self.score_img = resize_image(pygame.image.load('./assets/images/menu/score.png'), 50)
        self.options_img = resize_image(pygame.image.load('./assets/images/menu/options.png'), 45)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake II")

    def show(self):
        """Affiche le menu principal"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.screen_width // 2 - self.jouer_img.get_width() // 2 <= x <= self.screen_width // 2 + self.jouer_img.get_width() // 2 and 400 <= y <= 400 + self.jouer_img.get_height():
                        game = SnakeGame(self.background_img)
                        game.run()
                        return
                    elif self.screen_width // 2 - self.score_img.get_width() // 2 <= x <= self.screen_width // 2 + self.score_img.get_width() // 2 and 500 <= y <= 500 + self.score_img.get_height():
                        scores_page = ScorePage(self.background_img)
                        scores_page.show()
                    elif self.screen_width // 2 - self.options_img.get_width() // 2 <= x <= self.screen_width // 2 + self.options_img.get_width() // 2 and 600 <= y <= 600 + self.options_img.get_height():
                        options_page = OptionsPage(self.background_img)
                        options_page.show()

            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.logo_img, (self.screen_width // 2 - self.logo_img.get_width() // 2, 200))
            self.screen.blit(self.jouer_img, (self.screen_width // 2 - self.jouer_img.get_width() // 2, 400))
            self.screen.blit(self.score_img, (self.screen_width // 2 - self.score_img.get_width() // 2, 500))
            self.screen.blit(self.options_img, (self.screen_width // 2 - self.options_img.get_width() // 2, 600))
            pygame.display.flip()


class ScorePage:
    """Classe représentant la page des scores"""
    def __init__(self, background_img):
        self.screen_width = 500
        self.screen_height = 900
        self.background_img = background_img
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def show(self):
        """Affiche les scores"""
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        font = pygame.font.Font(None, 36)
        while True:
            self.screen.blit(self.background_img, (0, 0))
            title = font.render("Scores des parties", True, (255, 255, 255))
            self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

            for i, score in enumerate(scores):
                score_text = font.render(f"Partie {i + 1}: {score} points", True, (255, 255, 255))
                self.screen.blit(score_text, (50, 100 + i * 40))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return


class OptionsPage:
    """Classe représentant la page des options"""
    def __init__(self, background_img):
        self.screen_width = 500
        self.screen_height = 900
        self.background_img = background_img
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def show(self):
        """Affiche la page des options"""
        font = pygame.font.Font(None, 36)
        while True:
            self.screen.blit(self.background_img, (0, 0))
            title = font.render("Options", True, (255, 255, 255))
            self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

            info = font.render("Appuyez sur une touche pour revenir", True, (255, 255, 255))
            self.screen.blit(info, (50, 150))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return


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
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        scores.append(self.score)

        with open("scores.json", "w") as file:
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


if __name__ == "__main__":
    pygame.init()
    background_img = pygame.image.load('./assets/images/menu/background.png')
    background_img = pygame.transform.scale(background_img, (500, 900))
    menu = Menu(background_img)
    menu.show()
