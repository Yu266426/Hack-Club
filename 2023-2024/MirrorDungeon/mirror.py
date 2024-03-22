import pygame
import pygbase

from consts import TILE_SIZE


class HorizontalMirror:
	def __init__(self, tile_pos: tuple, tile_length: int) -> None:
		self.tile_pos = tile_pos
		self.pos = pygame.Vector2(tile_pos) * TILE_SIZE

		self.tile_length = tile_length
		self.length = tile_length * TILE_SIZE

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		pygame.draw.line(surface, "white", camera.world_to_screen(self.pos), camera.world_to_screen(self.pos + pygame.Vector2(self.length, 0)), width=5)
