import random

import pygame


class LargeAsteroid:
	def __init__(self, image: pygame.Surface, pos):
		self.base_image = image
		self.pos = pygame.Vector2(pos)
		self.base_rect = self.base_image.get_rect(center=self.pos)

		self.angle = random.uniform(0.0, 360.0)
		self.rotation_speed = random.uniform(20.0, 50.0) * (-1 if random.random() < 0.5 else 1)

		self.speed = random.uniform(100.0, 320.0)

		self.image = self.base_image
		self.rect = self.base_rect

		self.health = 20

	def update(self, delta):
		self.angle += self.rotation_speed * delta
		self.pos.y += self.speed * delta
		self.base_rect.center = self.pos

		self.image = pygame.transform.rotate(self.base_image, self.angle)
		self.rect = self.image.get_rect(center=self.base_rect.center)

	def draw(self, screen: pygame.Surface):
		screen.blit(self.image, self.rect)
