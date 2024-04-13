import pygame
import pygbase

from consts import TILE_SIZE


class HorizontalMirror:
	def __init__(self, tile_pos: tuple) -> None:
		self.tile_pos = tile_pos
		self.pos = pygame.Vector2(tile_pos) * TILE_SIZE

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		pygame.draw.rect(surface, "grey", (camera.world_to_screen(self.pos), (TILE_SIZE, TILE_SIZE)), width=3)


class VerticalMirror:
	def __init__(self, tile_pos: tuple) -> None:
		self.tile_pos = tile_pos
		self.pos = pygame.Vector2(tile_pos) * TILE_SIZE

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		pygame.draw.line(surface, "grey", camera.world_to_screen(self.pos + (TILE_SIZE / 2, 0)), camera.world_to_screen(self.pos + (TILE_SIZE / 2, TILE_SIZE)), width=6)
