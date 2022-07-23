import random

import pygame

from data.modules.game.contants import WINDOW_SIZE
from data.modules.game.game_object import GameObject
from data.modules.game.group import Group


class Star(GameObject):
	def __init__(self, pos, size_range=(2, 7)):
		self.pos = pygame.Vector2(pos)

		self.size: float = random.randint(size_range[0] * 100, size_range[1] * 100) / 100

	def update(self, delta: float, scroll: pygame.Vector2):
		scroll_pos = self.pos - scroll * (self.size / 10)

		if scroll_pos.x >= WINDOW_SIZE[0] + 20:
			self.pos.x -= WINDOW_SIZE[0] + 20
		elif scroll_pos.x <= -20:
			self.pos.x += WINDOW_SIZE[0] + 20

		if scroll_pos.y >= WINDOW_SIZE[1] + 20:
			self.pos.y -= WINDOW_SIZE[0] + 20
		elif scroll_pos.y <= -20:
			self.pos.y += WINDOW_SIZE[1] + 20

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		pygame.draw.rect(display, "white", pygame.Rect(self.pos - scroll * (self.size / 10), (self.size, self.size)))


def generate_stars(star_group: Group, amount: int):
	for _ in range(amount):
		star_group.add(Star((random.randint(-20, WINDOW_SIZE[0] + 20), random.randint(-20, WINDOW_SIZE[1] + 20))))
