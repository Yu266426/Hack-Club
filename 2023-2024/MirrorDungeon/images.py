import pygame

images = {}


def load_image(name):
	images[name] = pygame.image.load(f"{name}.png").convert_alpha()
