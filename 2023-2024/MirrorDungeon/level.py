import pygame
import pygbase

from tile import Tile


class Level:
	def __init__(self):
		self.TILE_SIZE = 16 * 5

		self.n_rows = 0
		self.n_cols = 0
		self.tiles: list[list[Tile]] = []

		self.load()

	def get_tile_pos(self, pos, offset=(0, 0)):
		return int((pos.x + offset[0]) // self.TILE_SIZE), int((pos.y + offset[1]) // self.TILE_SIZE)

	def check_bounds(self, tile_pos):
		return 0 <= tile_pos[0] < self.n_cols and 0 <= tile_pos[1] < self.n_rows

	def load(self):
		tile_mapping = {
			0: ("floor_tiles", 0, False),
			1: ("wall_tiles", 0, True)
		}

		temp_map = [
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		]

		self.n_rows = len(temp_map)
		self.n_cols = len(temp_map[0])

		for row_index, row in enumerate(temp_map):
			self.tiles.append([])
			for col_index, tile in enumerate(row):
				self.tiles[row_index].append(Tile((col_index * self.TILE_SIZE, row_index * self.TILE_SIZE), *tile_mapping[tile]))

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for row in self.tiles:
			for tile in row:
				tile.draw(surface, camera)
