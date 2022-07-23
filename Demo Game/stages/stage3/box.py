import random

import pygame


class Box:
	def __init__(self, spawn_pos):
		# Generates a random size
		size = (random.randint(20, 60), random.randint(60, 130))

		# Generates random speed
		self.speed = random.randint(7, 14)

		# Similar to player, with image defaulting to black
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect(center=spawn_pos)

		# Gets display
		self.display = pygame.display.get_surface()

	def update(self):
		self.rect.y += self.speed

	def draw(self):
		self.display.blit(self.image, self.rect)
