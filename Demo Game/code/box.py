import random

import pygame


class Box:
	def __init__(self, spawn_pos):
		# Generates a random size
		size = (random.randint(20, 60), random.randint(60, 130))

		# Generates random speed
		self.speed = random.randint(7, 14)

		self.pos = pygame.Vector2(spawn_pos)

		# Similar to player, with image defaulting to black
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect(center=self.pos)

		# Gets display
		self.display = pygame.display.get_surface()

	def update(self, delta):
		self.pos.y += self.speed * delta
		self.rect.center = self.pos

	def draw(self):
		self.display.blit(self.image, self.rect)
