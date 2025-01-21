import pygame
import sys
import random
import json
from core.menu import Menu

if __name__ == "__main__":
    pygame.init()
    background_img = pygame.image.load('./assets/images/menu/background.png')
    background_img = pygame.transform.scale(background_img, (500, 900))
    menu = Menu(background_img)
    menu.show()
