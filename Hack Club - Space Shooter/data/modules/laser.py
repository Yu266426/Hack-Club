import pygame

from data.modules.image import Image


class Laser:
	def __init__(self, pos, angle):
		self.pos = pygame.Vector2(pos)

		self.image = Image("laser", 3, angle)

		self.movement = pygame.Vector2(0, 1).rotate(-angle - 90) * 15

	def update(self):
		self.pos += self.movement

	def draw(self, window: pygame.Surface):
		self.image.draw(window, self.pos)
