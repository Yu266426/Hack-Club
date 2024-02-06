import pygame
import pygbase

from tile import Tile


class Level:
	def __init__(self):
		self.tiles = [
			[Tile((0, 0), "floor_tiles", 0)]
		]

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for row in self.tiles:
			for tile in row:
				tile.draw(surface, camera)
