import pygame

def resize_image(image, desired_height):
    """Redimensionner une image en fonction de la hauteur désirée"""
    height = image.get_height()
    width = image.get_width()
    ratio = width / height
    new_width = int(desired_height * ratio)
    return pygame.transform.scale(image, (new_width, desired_height))
