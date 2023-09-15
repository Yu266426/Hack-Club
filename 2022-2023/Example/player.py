import math

import pygame

from image import Image
from images import PLAYER_IMAGE


class Player:
	def __init__(self):
		self.pos = pygame.Vector2((400, 400))

		self.image = Image(PLAYER_IMAGE, (50, 50))

		self.rect = self.image.get_rect(self.pos)

		self.input = pygame.Vector2()

		self.speed = 2
		self.drag = 0.1

		self.acceleration = pygame.Vector2()
		self.velocity = pygame.Vector2()

	def move(self):
		self.acceleration = self.input * self.speed

		self.velocity += self.acceleration
		self.velocity -= self.velocity * self.drag

		self.pos += self.velocity

		self.rect.center = self.pos

		# Checking Bounds
		if self.rect.left > 800:
			self.rect.right = 0
			self.pos.update(self.rect.center)

		elif self.rect.right < 0:
			self.rect.left = 800
			self.pos.update(self.rect.center)

		if self.rect.top > 800:
			self.rect.bottom = 0
			self.pos.update(self.rect.center)
		elif self.rect.bottom < 0:
			self.rect.top = 800
			self.pos.update(self.rect.center)

	def update(self):
		keys = pygame.key.get_pressed()
		self.input.x = keys[pygame.K_d] - keys[pygame.K_a]
		self.input.y = keys[pygame.K_s] - keys[pygame.K_w]

		self.move()

		if self.input.length() != 0:
			self.input.normalize_ip()

		mouse_pos = pygame.mouse.get_pos()
		self.image.angle = math.degrees(math.atan2(self.pos.y - mouse_pos[1], mouse_pos[0] - self.pos.x))

	def draw(self, screen):
		self.image.draw(screen, self.rect)
