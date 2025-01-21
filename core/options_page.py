import pygame
import sys

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

