import pygame
import pygbase
import random

from consts import TILE_SIZE
from mirror import Mirror
from tile import Tile, TopWallTile


class Level:
	def __init__(self):
		self.TILE_SIZE = 16 * 5

		self.num_rows = 0
		self.num_cols = 0
		self.tiles: list[list[list[Tile | None]]] = [[], []]  # [Floor, Wall]
		self.mirror_map_bitmask: list[list[int]] = []

		self.load()

	def get_tile_pos(self, pos, offset=(0, 0)) -> tuple[int, int]:
		return int((pos[0] + offset[0]) // TILE_SIZE), int((pos[1] + offset[1]) // TILE_SIZE)

	def check_bounds(self, tile_pos) -> bool:
		return 0 <= tile_pos[0] < self.num_cols and 0 <= tile_pos[1] < self.num_rows

	def check_tile_collidable(self, tile_pos, layer=1) -> bool:
		"""Deprecated"""
		return self.check_bounds(tile_pos) and self.tiles[layer][tile_pos[1]][tile_pos[0]] is not None and self.tiles[layer][tile_pos[1]][
		    tile_pos[0]].collidable

	def get_tile(self, tile_pos, layer=1) -> Tile | None:
		if self.check_bounds(tile_pos):
			return self.tiles[layer][tile_pos[1]][tile_pos[0]]
		else:
			return None

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
		    21: ("wall_tiles", 6, True, 0),
		    22: ("wall_tiles", 0, True),  # Top left
		    23: ("wall_tiles", 0, True, 1),  # Top left
		    24: ("wall_tiles", 1, True),  # Top right
		    25: ("wall_tiles", 1, True, 2),  # Top right
		    26: ("wall_tiles", 2, True, (4, 16)),  # Left
		    27: ("wall_tiles", 3, True, (4, 16), (12 * 5, 0)),  # Right
		    28: ("wall_tiles", 4, True, (4, 16)),  # Bottom left
		    29: ("wall_tiles", 5, True, (4, 16), (12 * 5, 0)),  # Bottom right
		    210: ("wall_alternates", 0, True),
		    211: ("wall_alternates", 1, True),
		    212: ("wall_alternates", 3, True)
		}

		floor_gen_settings = {
		    11: 0.02,
		    12: 0.02,
		    13: 0.02,
		    14: 0.02,
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
		  [2, 0, 0, 0, 0, 0, 2, 2, 2, 2],
		  [2, 0, 2, 0, 0, 0, 0, 0, 0, 2],
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
				tile_type = tile
				is_top_wall = True

				if tile == 2:
					# TODO: Redo this using a strategy of
					# marking adjacent tiles, then computing the wall type
					#
					# Potentially even precompute an adjacency map, then in the next pass compute tile type
					mark_tile_top = 0
					mark_tile_bottom = 0
					mark_tile_left = 0
					mark_tile_right = 0

					mark_tile_top_left = 0
					mark_tile_top_right = 0
					mark_tile_bottom_left = 0
					mark_tile_bottom_right = 0

					# Has tile on top
					if row_index > 0 and temp_map[1][row_index - 1][col_index] != 0:
						is_top_wall = False
						mark_tile_top = 1
					elif row_index == 0:
						mark_tile_top = 2

					# Has tile below
					if row_index < self.num_rows - 1 and temp_map[1][row_index + 1][col_index] != 0:
						mark_tile_bottom = 1
					elif row_index == self.num_rows - 1:
						mark_tile_bottom = 2

					# Has tile to the left
					if col_index > 0 and temp_map[1][row_index][col_index - 1] != 0:
						mark_tile_left = 1
					elif col_index == 0:
						mark_tile_left = 2

					# Has tile to the right
					if col_index < self.num_cols - 1 and temp_map[1][row_index][col_index + 1] != 0:
						mark_tile_right = 1
					elif col_index == self.num_cols - 1:
						mark_tile_right = 2

					# Has tile top left
					if row_index > 0 and col_index > 0 and temp_map[1][row_index - 1][col_index - 1] != 0:
						mark_tile_top_left = 1
					elif row_index == 0 and col_index == 0:
						mark_tile_top_left = 2

					# Has tile top right
					if row_index > 0 and col_index < self.num_cols - 1 and temp_map[1][row_index - 1][col_index + 1] != 0:
						mark_tile_top_right = 1
					elif row_index == 0 and col_index == self.num_cols - 1:
						mark_tile_bottom_right = 2

					# Has tile bottom left
					if row_index < self.num_rows - 1 and col_index > 0 and temp_map[1][row_index + 1][col_index - 1] != 0:
						mark_tile_bottom_left = 1
					elif row_index == self.num_rows - 1 and col_index == 0:
						mark_tile_bottom_left = 2

					# Has tile bottom right
					if row_index < self.num_rows - 1 and col_index < self.num_cols - 1 and temp_map[1][row_index + 1][col_index + 1] != 0:
						mark_tile_bottom_right = 1
					elif row_index == self.num_rows - 1 and col_index == self.num_cols - 1:
						mark_tile_bottom_right = 2

					match (mark_tile_top, mark_tile_bottom, mark_tile_left, mark_tile_right, mark_tile_top_left, mark_tile_top_right,
					       mark_tile_bottom_left, mark_tile_bottom_right):
					# Wall (tile)
						case (1,
						      *remaining) if not (remaining[1] == 0 and remaining[2] == 2) and not (remaining[1] == 2 and remaining[2] == 0) and not (
						          remaining[0] == 1 and remaining[3] != 1 and remaining[4] != 1 and remaining[5] != 1 and remaining[6] != 1):
							tile_type = 20
					# Wall (air)
						case (0, 0, 1, 1, *corners):
							tile_type = 21
						case (0, 0, 1, 0, *corners):
							tile_type = 21
						case (0, 0, 0, 1, *corners):
							tile_type = 21
						case (0, 0, 0, 0, *corners):
							tile_type = 21
						case (0, 1, 1, 1, *corners):
							tile_type = 21
						case (0, 1, 1, 0, *corners):
							tile_type = 21
						case (0, 1, 0, 1, *corners):
							tile_type = 21
						case (0, 1, 0, 0, *corners):
							tile_type = 21
						case (0, 2, 1, 1, *corners):
							tile_type = 21
						case (0, 2, 1, 0, *corners):
							tile_type = 21
						case (0, 2, 0, 1, *corners):
							tile_type = 21
						case (0, 2, 0, 0, *corners):
							tile_type = 21
					# Wall (void)
						case (2, 0, 1, 1, *corners):
							tile_type = 21
						case (2, 0, 1, 0, *corners):
							tile_type = 21
						case (2, 0, 0, 1, *corners):
							tile_type = 21
						case (2, 0, 0, 0, *corners):
							tile_type = 21
						case (2, 1, 1, 1, *corners):
							tile_type = 21
						case (2, 1, 1, 0, *corners):
							tile_type = 21
						case (2, 1, 0, 1, *corners):
							tile_type = 21
						case (2, 1, 0, 0, *corners):
							tile_type = 21
						case (2, 2, 1, 1, *corners):
							tile_type = 21
						case (2, 2, 1, 0, *corners):
							tile_type = 21
						case (2, 2, 0, 1, *corners):
							tile_type = 21
						case (2, 2, 0, 0, *corners):
							tile_type = 21

					# Top left (tile) Invalid?
					# case (1, 1, 0, 1, *corners):
					# 	tile_type = 22
					# case (1, 1, 2, 1, *corners):
					# 	tile_type = 22
					# case (1, 2, 2, 1, *corners):
					# 	tile_type = 22
					# Top left (void | air)
						case (0, 1, 0, 1, *corners):
							tile_type = 23
						case (0, 1, 2, 1, *corners):
							tile_type = 23
						case (2, 1, 0, 1, *corners):
							tile_type = 23
						case (2, 1, 2, 1, *corners):
							tile_type = 23
						case (1, 1, 0, 1, *corners) if 1 not in corners:
							tile_type = 22
						case (1, 1, 2, 1, *corners) if 1 not in corners:
							tile_type = 22
					# Top right (tile) Invalid?
					# case (1, 1, 1, 0, *corners):
					# 	tile_type = 24
					# case (1, 1, 1, 2, *corners):
					# 	tile_type = 24
					# case (1, 2, 1, 2, *corners):
					# 	tile_type = 24
					# Top right (void | air)
						case (0, 1, 1, 0, *corners):
							tile_type = 25
						case (0, 1, 1, 2, *corners):
							tile_type = 25
						case (2, 1, 1, 0, *corners):
							tile_type = 25
						case (2, 1, 1, 2, *corners):
							tile_type = 25
						case (1, 1, 1, *remaining) if 1 not in remaining:
							tile_type = 24
					# Left
						case (1, 1, 0, 0, *corners) if corners[3] == 0:
							tile_type = 26
						case (1, 1, 1, 0, *corners) if corners[3] == 0:
							tile_type = 26
						case (1, 1, 2, 0, *corners) if corners[3] == 0:
							tile_type = 26
					# Right
						case (1, 1, 0, 0, *corners) if corners[2] == 0:
							tile_type = 27
						case (1, 1, 0, 1, *corners) if corners[2] == 0:
							tile_type = 27
						case (1, 1, 0, 2, *corners) if corners[2] == 0:
							tile_type = 27
						case (1, 1, 1, 2, *corners) if corners[2] == 0:
							tile_type = 27
					# Bottom Left (tile)
						case (1, 1, 0, 0, *corners) if corners[3] == 1:
							tile_type = 28
						case (1, 1, 2, 0, *corners):
							tile_type = 28
						case (1, 2, 0, 0, *corners) if corners[3] == 1:
							tile_type = 28
						case (1, 2, 2, 0, *corners):
							tile_type = 28
					# Bottom Right (tile)
						case (1, 1, 0, 0, *corners) if corners[2] == 1:
							tile_type = 29
						case (1, 1, 0, 2, *corners) if corners[2] == 1:
							tile_type = 29
						case (1, 2, 0, 0, *corners) if corners[2] == 1:
							tile_type = 29
						case (1, 2, 0, 2, *corners) if corners[2] == 1:
							tile_type = 29
					# Catch remaining cases
						case _:
							print(f"Wall at row: {row_index} and col: {col_index} is not resolved")
							tile_type = 0

					print(tile_type, row_index, col_index, (mark_tile_top, mark_tile_bottom, mark_tile_left, mark_tile_right, mark_tile_top_left,
					                                        mark_tile_top_right, mark_tile_bottom_left, mark_tile_bottom_right))

				if tile_type == 0:
					self.tiles[1][row_index].append(None)
					continue

				if is_top_wall:
					self.tiles[1][row_index].append(TopWallTile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]))
				else:
					self.tiles[1][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]))

	def generate_mirror_map(self):
		pass

	def draw_layer(self, surface: pygame.Surface, camera: pygbase.Camera, layer: int):
		for row in self.tiles[layer]:
			for tile in row:
				if tile:
					tile.draw(surface, camera)

	def draw_layer_with_entites(self, surface: pygame.Surface, camera: pygbase.Camera, layer: int, entities: list):
		# Sort entites
		sorted_entities = sorted(entities, key=lambda e: e.pos.y * self.num_cols * self.TILE_SIZE + e.pos.x)

		current_entity_index = 0
		for row_index, row in enumerate(self.tiles[layer]):
			for entity in sorted_entities[current_entity_index:]:
				if self.get_tile_pos((entity.pos.x, entity.pos.y - 1))[1] != row_index:
					break

				entity.draw(surface, camera)

				current_entity_index += 1

			for tile in row:
				if tile:
					tile.draw(surface, camera)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for layer in self.tiles:
			for row in layer:
				for tile in row:
					if tile:
						tile.draw(surface, camera)
