import random

import pygame


class Box:
	def __init__(self):
		self.speed = random.randint(10, 20)

		self.image = pygame.Surface((random.randint(30, 70), random.randint(50, 100)))
		self.image.fill("black")

		self.rect = self.image.get_rect(midbottom=(random.randint(20, 480), 0))

	def update(self):
		self.rect.y += self.speed

	def draw(self, surface):
		surface.blit(self.image, self.rect)
