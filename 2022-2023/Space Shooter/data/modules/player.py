import pygame

from data.modules.image import Image
from data.modules.utils import get_angle_to


class Player:
	acceleration = 1.3
	drag = 0.12

	def __init__(self, pos):
		self.pos = pygame.Vector2(pos)

		self.input = pygame.Vector2()

		self.acceleration = pygame.Vector2()
		self.movement = pygame.Vector2()

		self.image = Image("player", scale=6)

		self.alive = True
		self.health = 100
		self.radius = 20

	def damage(self, damage):
		self.health -= damage

		if self.health <= 0:
			self.alive = False
			return True
		return False

	def get_inputs(self, scroll):
		keys_pressed = pygame.key.get_pressed()

		self.input.x = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
		self.input.y = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]

		self.image.angle = get_angle_to(self.pos - scroll, pygame.mouse.get_pos())

	def move(self, delta):
		if self.input.length() != 0:
			self.acceleration = self.input.normalize() * Player.acceleration
		else:
			self.acceleration.xy = 0, 0

		self.acceleration -= Player.drag * self.movement

		self.movement += self.acceleration * delta

		self.pos += self.movement * delta

	def update(self, delta, scroll):
		self.get_inputs(scroll)

		self.move(delta)

	def draw(self, surface, scroll):
		self.image.draw(surface, self.pos - scroll)
