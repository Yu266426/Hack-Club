import pygame
import pygbase
from consts import PLAYER_HEIGHT, PLAYER_WIDTH

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

		self.level.draw_layer(surface, self.camera, 0)
		self.level.draw_layer_with_entites(surface, self.camera, 1, [self.player])

		pygame.draw.rect(surface, "white",pygame.Rect(self.camera.world_to_screen((self.player.pos.x - PLAYER_WIDTH / 2, self.player.pos.y - PLAYER_HEIGHT)), (PLAYER_WIDTH, PLAYER_HEIGHT)))
