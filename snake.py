import pygame

# Initialisation de pygame
pygame.init()

# Dimensions de l'écran
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game - Étape 1')

# Couleur de fond
black = (0, 0, 0)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec la couleur de fond
    screen.fill(black)
    pygame.display.update()

pygame.quit()
