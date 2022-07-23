import pygame

from data.modules.components.position import Position


class GameObject:
	def __init__(self, pos, radius, angle=0):
		self.pos = Position(pos, radius, angle=angle)

	def update(self, delta: float, scroll: pygame.Vector2):
		pass

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		pass

	def check_death(self):
		return False
