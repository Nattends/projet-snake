import pygame
import sys

from utils.helpers import resize_image
from .snake_game import SnakeGame
from .score_page import ScorePage
from .options_page import OptionsPage


class Menu:
    """Classe représentant le menu principal"""
    def __init__(self, background_img):
        self.screen_width = 500
        self.screen_height = 900
        self.background_img = background_img
        self.logo_img = resize_image(pygame.image.load('assets/images/menu/logo.png'), 80)

        # Images normales
        self.jouer_img = resize_image(pygame.image.load('assets/images/menu/jouer.png'), 50)
        self.score_img = resize_image(pygame.image.load('assets/images/menu/score.png'), 50)
        self.options_img = resize_image(pygame.image.load('assets/images/menu/options.png'), 45)

        # Images hover
        self.jouer_img_hover = resize_image(pygame.image.load('assets/images/menu/jouer_white.png'), 50)
        self.score_img_hover = resize_image(pygame.image.load('assets/images/menu/score_white.png'), 50)
        self.options_img_hover = resize_image(pygame.image.load('assets/images/menu/options_white.png'), 45)

        # États de hover
        self.jouer_hovered = False
        self.score_hovered = False
        self.options_hovered = False

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

                # Détecter les hover
                elif event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()

                    self.jouer_hovered = (
                        self.screen_width // 2 - self.jouer_img.get_width() // 2 <= x <= self.screen_width // 2 + self.jouer_img.get_width() // 2
                        and 400 <= y <= 400 + self.jouer_img.get_height()
                    )
                    self.score_hovered = (
                        self.screen_width // 2 - self.score_img.get_width() // 2 <= x <= self.screen_width // 2 + self.score_img.get_width() // 2
                        and 500 <= y <= 500 + self.score_img.get_height()
                    )
                    self.options_hovered = (
                        self.screen_width // 2 - self.options_img.get_width() // 2 <= x <= self.screen_width // 2 + self.options_img.get_width() // 2
                        and 600 <= y <= 600 + self.options_img.get_height()
                    )

                    print(f"Jouer: {self.jouer_hovered}, Score: {self.score_hovered}, Options: {self.options_hovered}")

            # Dessiner le fond
            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.logo_img, (self.screen_width // 2 - self.logo_img.get_width() // 2, 200))

            # Changer les images en fonction du hover
            jouer_img_to_draw = self.jouer_img_hover if self.jouer_hovered else self.jouer_img
            score_img_to_draw = self.score_img_hover if self.score_hovered else self.score_img
            options_img_to_draw = self.options_img_hover if self.options_hovered else self.options_img

            self.screen.blit(jouer_img_to_draw, (self.screen_width // 2 - self.jouer_img.get_width() // 2, 400))
            self.screen.blit(score_img_to_draw, (self.screen_width // 2 - self.score_img.get_width() // 2, 500))
            self.screen.blit(options_img_to_draw, (self.screen_width // 2 - self.options_img.get_width() // 2, 600))

            pygame.display.flip()  # Rafraîchissement de l'affichage
