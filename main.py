import pygame
import sys

def resize_image(image, desired_height):
    """Redimensionner une image en fonction de la hauteur désirée"""
    # Obtenir les dimensions de l'image
    height = image.get_height()  # Hauteur de l'image
    width = image.get_width()   # Largeur de l'image

    # Calculer le ratio largeur/hauteur
    ratio = width / height

    # Calculer la largeur correspondant à cette hauteur en fonction du ratio
    new_width = int(desired_height * ratio)

    # Redimensionner l'image avec les nouvelles dimensions
    return pygame.transform.scale(image, (new_width, desired_height))

class Menu:
    """Classe représentant le menu du jeu"""
    def __init__(self):
        """Méthode d'initialisation de la classe Menu"""
        pygame.init()

        # Initialiser la fenêtre pygame
        self.screen_width = 500
        self.screen_height = 900

        # Initialiser le background
        self.background_img = pygame.image.load('./assets/images/menu/background.png')
        self.background_img = pygame.transform.scale(self.background_img, (self.screen_width, self.screen_height))

        # Initialiser le logo
        self.logo_img = pygame.image.load('./assets/images/menu/logo.png')
        self.logo_img = resize_image(self.logo_img, 80)

        # Initialiser le bouton jouer
        self.jouer_img = pygame.image.load('./assets/images/menu/jouer.png')
        self.jouer_img = resize_image(self.jouer_img, 50)

        # Initialiser le bouton score
        self.score_img = pygame.image.load('./assets/images/menu/score.png')
        self.score_img = resize_image(self.score_img, 50)

        # Initialiser le bouton options
        self.options_img = pygame.image.load('./assets/images/menu/options.png')
        self.options_img = resize_image(self.options_img, 45)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake II")

    def show(self):
        """Méthode pour afficher le menu"""
        while True:
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Obtenir les coordonnées de la souris
                    x, y = pygame.mouse.get_pos()

                    # Vérifier si le joueur clique sur les boutons
                    if self.screen_width // 2 - self.jouer_img.get_width() // 2 <= x <= self.screen_width // 2 + self.jouer_img.get_width() // 2 and 400 <= y <= 400 + self.jouer_img.get_height():
                        print("Jouer")
                    elif self.screen_width // 2 - self.score_img.get_width() // 2 <= x <= self.screen_width // 2 + self.score_img.get_width() // 2 and 500 <= y <= 500 + self.score_img.get_height():
                        print("Score")
                    elif self.screen_width // 2 - self.options_img.get_width() // 2 <= x <= self.screen_width // 2 + self.options_img.get_width() // 2 and 600 <= y <= 600 + self.options_img.get_height():
                        print("Options")

            # Afficher le fond d'écran
            self.screen.blit(self.background_img, (0, 0))

            #
            self.screen.blit(self.logo_img, (self.screen_width // 2 - self.logo_img.get_width() // 2, 200))
            self.screen.blit(self.jouer_img, (self.screen_width // 2 - self.jouer_img.get_width() // 2, 400))
            self.screen.blit(self.score_img, (self.screen_width // 2 - self.score_img.get_width() // 2, 500))
            self.screen.blit(self.options_img, (self.screen_width // 2 - self.options_img.get_width() // 2, 600))

            # Mettre à jour l'affichage
            pygame.display.flip()

    def hide(self):
        """Méthode pour cacher le menu"""
        pass

if __name__ == "__main__":
    menu = Menu()
    menu.show()
