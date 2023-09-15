import pygame

from data.modules.image import Image
from data.modules.utils import get_angled_offset


class Laser:
	def __init__(self, pos, direction):
		self.image = Image("laser", angle=direction, scale=2.2)

		self.pos = pygame.Vector2(pos)
		self.movement = get_angled_offset(direction, 20)

		self.radius = 2

	def update(self, delta):
		self.pos += self.movement * delta

	def draw(self, surface: pygame.Surface, scroll):
		self.image.draw(surface, self.pos - scroll)
