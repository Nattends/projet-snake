import pygame
import json
import sys

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
            with open("data/scores.json", "r") as file:
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
