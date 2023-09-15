import random

import pygame

from data.modules.constants import SCREEN_WIDTH, SCREEN_HEIGHT

colours = [
	(255, 255, 255),
	(255, 255, 204),
	(230, 255, 255),
	(255, 217, 179)
]


class Star:
	def __init__(self, pos, scale):
		self.pos = pygame.Vector2(pos)

		self.scale = scale

		self.colour = random.choice(colours)

	def get_scrolled_pos(self, scroll):
		return self.pos - scroll * self.scale / 10

	def update(self, delta, scroll):
		scrolled_pos = self.get_scrolled_pos(scroll)

		if scrolled_pos.x < -10:
			self.pos.x += SCREEN_WIDTH + 10
		if SCREEN_WIDTH + 10 < scrolled_pos.x:
			self.pos.x -= SCREEN_WIDTH + 10

		if scrolled_pos.y < -10:
			self.pos.y += SCREEN_HEIGHT + 10
		if SCREEN_HEIGHT + 10 < scrolled_pos.y:
			self.pos.y -= SCREEN_HEIGHT + 10

	def draw(self, surface, scroll):
		pygame.draw.rect(surface, self.colour, (self.get_scrolled_pos(scroll), (self.scale, self.scale)))
