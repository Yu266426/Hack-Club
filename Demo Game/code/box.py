import random

import pygame


class Box:
	def __init__(self, spawn_pos):
		size = (random.randint(20, 60), random.randint(60, 130))

		self.speed = random.randint(7, 14)

		self.pos = pygame.Vector2(spawn_pos)

		self.image = pygame.Surface(size)
		self.image.fill((24, 154, 180))
		self.rect = self.image.get_rect(center=self.pos)

		self.display = pygame.display.get_surface()

	def update(self, delta):
		self.pos.y += self.speed * delta
		self.rect.center = self.pos

	def draw(self):
		self.display.blit(self.image, self.rect)
