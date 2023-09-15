import random

import pygame

from data.modules.constants import AsteroidTypes
from data.modules.image import Image
from data.modules.utils import get_angled_offset


class Asteroid:
	def __init__(self, asteroid_type, pos, direction):
		self.pos = pygame.Vector2(pos)

		self.type = asteroid_type

		if asteroid_type == AsteroidTypes.Large:
			self.image = Image("large asteroid", angle=random.randint(0, 360), scale=5)
			self.movement = get_angled_offset(direction, random.randint(3, 7))
			self.spin = float(random.randint(-10, 10)) / 10.0

			self.health = 20

			self.radius = 100
		else:
			self.image = Image("medium asteroid", angle=random.randint(0, 360), scale=5)
			self.movement = get_angled_offset(direction, random.randint(4, 8))
			self.spin = float(random.randint(-10, 10)) / 5.0

			self.health = 10

			self.radius = 60

	def damage(self, damage=0):
		self.health -= damage
		if self.health <= 0:
			return True
		return False

	def update(self, delta):
		self.pos += self.movement * delta

		self.image.angle += self.spin * delta

	def draw(self, surface, scroll):
		self.image.draw(surface, self.pos - scroll)
