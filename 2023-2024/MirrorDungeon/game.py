import pygame
import pygbase

from level import Level
from player import Player


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()

		self.camera = pygbase.Camera()

		self.level = Level()

		self.player = Player((400, 400), self.level)

	def update(self, delta: float):
		self.player.update(delta)
		self.camera.lerp_to_target(self.player.pos - pygame.Vector2(400, 400), 1.3 * delta)

	def draw(self, surface: pygame.Surface):
		surface.fill("black")

		self.level.draw(surface, self.camera)

		self.player.draw(surface, self.camera)
