import pygame

from data.modules.game.game_object import GameObject


class Group:
	def __init__(self):
		self.objects: list[GameObject] = []

	def add(self, game_object: GameObject):
		self.objects.append(game_object)

	def remove(self, game_object: GameObject):
		if game_object in self.objects:
			self.objects.remove(game_object)

	def update(self, delta: float, scroll: pygame.Vector2):
		for game_object in self.objects:
			game_object.update(delta, scroll)

	def check_death(self):
		for game_object in self.objects:
			if game_object.check_death():
				self.objects.remove(game_object)

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		for game_object in self.objects:
			game_object.draw(display, scroll)
