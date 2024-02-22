import pygame
import pygbase
import random

from consts import TILE_SIZE
from tile import Tile


class Level:
	def __init__(self):
		self.TILE_SIZE = 16 * 5

		self.n_rows = 0
		self.n_cols = 0
		self.tiles: list[list[list[Tile | None]]] = [[], []]

		self.load()

	def get_tile_pos(self, pos, offset=(0, 0)):
		return int((pos[0] + offset[0]) // TILE_SIZE), int((pos[1] + offset[1]) // TILE_SIZE)

	def check_bounds(self, tile_pos):
		return 0 <= tile_pos[0] < self.num_cols and 0 <= tile_pos[1] < self.num_rows

	def check_tile_collidable(self, tile_pos, layer=1):
		return self.check_bounds(tile_pos) and self.tiles[layer][tile_pos[1]][tile_pos[0]] is not None and self.tiles[layer][tile_pos[1]][
		    tile_pos[0]].collidable

	def load(self):
		tile_mapping = {
		    # 1 is used to mark procedural floors
		    10: ("floor_tiles", 0, False),
		    11: ("floor_tiles", 1, False),
		    12: ("floor_tiles", 2, False),
		    13: ("floor_tiles", 3, False),
		    14: ("floor_tiles", 4, False),
		    15: ("floor_tiles", 5, False),
		    16: ("floor_tiles", 6, False),
		    17: ("floor_tiles", 7, False),
		    # 2 is used to mark procedural walls
		    20: ("wall_tiles", 6, True),
		    21: ("wall_alternates", 0, True),
		    22: ("wall_alternates", 1, True),
		    23: ("wall_alternates", 3, True)
		}

		floor_gen_settings = {
		    11: 0.02,
		    12: 0.02,
		    13: 0.02,
		    14: 0.02,
		    15: 0.02,
		    16: 0.02,
		    17: 0.02,
		}

		temp_map = [
		 [  # Floor
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		 ],
		 [  # Wall
		  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
		 ]
		]  # yapf: disable

		self.num_rows = len(temp_map[0])
		self.num_cols = len(temp_map[0][1])

		# Generate floor
		alternate_floor_total_percentage = 0
		for value in floor_gen_settings.values():
			alternate_floor_total_percentage += value
		default_floor_gen_chance = 1 - alternate_floor_total_percentage

		for row_index, row in enumerate(temp_map[0]):
			self.tiles[0].append([])
			for col_index, tile in enumerate(row):
				if tile == 0:
					self.tiles[0][row_index].append(None)
					continue

				tile_type = tile

				if tile_type == 1:
					random_value = random.random()

					if random_value < default_floor_gen_chance:
						tile_type = 10
					else:
						gen_sum = 0
						for _tile_type, gen_weight in floor_gen_settings.items():
							gen_sum += gen_weight

							if random_value < default_floor_gen_chance + gen_sum:
								tile_type = _tile_type
								break

				self.tiles[0][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]))

		# Wall generation
		for row_index, row in enumerate(temp_map[1]):
			self.tiles[1].append([])
			for col_index, tile in enumerate(row):
				if tile == 0:
					self.tiles[1][row_index].append(None)
					continue

				tile_type = tile

				if tile == 2:
					random_value = random.random()

					if random_value < 0.7:
						tile_type = 20  # Regular wall
					elif random_value < 0.8:
						tile_type = 21  # Banner Red
					elif random_value < 0.9:
						tile_type = 22  # Banner Blue
					else:
						tile_type = 23

				self.tiles[1][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]))

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for layer in self.tiles:
			for row in layer:
				for tile in row:
					if tile:
						tile.draw(surface, camera)
