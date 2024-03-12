import random

import pygame
import pygbase
from pygbase.resources import json

from consts import TILE_SIZE
from files import LEVELS_DIR
from tile import Tile, TopWallTile


class Level:
	def __init__(self, name: str, size: tuple[int, int] = (10, 10)):
		self.TILE_SIZE = 16 * 5

		self.num_rows = size[1]
		self.num_cols = size[0]
		self.tiles: list[list[list[Tile | None]]] = [[], []]  # [Floor, Wall]
		self.mirror_map_bitmask: list[list[int]] = []

		self.load(name)

	@staticmethod
	def get_tile_pos(pos, offset=(0, 0)) -> tuple[int, int]:
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

	def load(self, name: str):
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

		floor_gen_mapping = {
			"large_crack": 11,
			"medium_crack": 12,
			"bottom_left_hole": 13,
			"small_crack": 14,
			"bottom_right_hole": 15,
			"top_right_hole": 16,
			"top_left_hole": 17
		}

		file_path = LEVELS_DIR / f"{name}.json"
		if not file_path.exists():
			data: dict = {
				"tiles": {
					"floor": [[1 for _ in range(self.num_cols)] for _ in range(self.num_rows)],
					"wall": [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
				},
				"floor_gen_settings": {
					"large_crack": 0.02,
					"medium_crack": 0.02,
					"small_crack": 0.02,
					"bottom_left_hole": 0.02,
					"bottom_right_hole": 0.02,
					"top_right_hole": 0.02,
					"top_left_hole": 0.02
				}
			}

			for col in range(self.num_cols):
				data["tiles"]["wall"][0][col] = 2
				data["tiles"]["wall"][self.num_rows - 1][col] = 2

			for row in range(self.num_rows):
				data["tiles"]["wall"][row][0] = 2
				data["tiles"]["wall"][row][self.num_cols - 1] = 2

			# Create new level file
			with open(file_path, "w") as level_file:
				level_file.write(json.dumps(data))
		else:
			# Load level file
			with open(file_path) as level_file:
				data = json.load(level_file)

		floor_tiles: list[list[int]] = data["tiles"]["floor"]
		wall_tiles: list[list[int]] = data["tiles"]["wall"]

		floor_gen_settings = {floor_gen_mapping[floor_type]: percentage for floor_type, percentage in data["floor_gen_settings"].items()}

		# Generate floor
		alternate_floor_total_percentage = 0
		for value in floor_gen_settings.values():
			alternate_floor_total_percentage += value
		default_floor_gen_chance = 1 - alternate_floor_total_percentage

		for row_index, row in enumerate(floor_tiles):
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
		for row_index, row in enumerate(wall_tiles):
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
					if row_index > 0 and wall_tiles[row_index - 1][col_index] != 0:
						is_top_wall = False
						mark_tile_top = 1
					elif row_index == 0:
						mark_tile_top = 2

					# Has tile below
					if row_index < self.num_rows - 1 and wall_tiles[row_index + 1][col_index] != 0:
						mark_tile_bottom = 1
					elif row_index == self.num_rows - 1:
						mark_tile_bottom = 2

					# Has tile to the left
					if col_index > 0 and wall_tiles[row_index][col_index - 1] != 0:
						mark_tile_left = 1
					elif col_index == 0:
						mark_tile_left = 2

					# Has tile to the right
					if col_index < self.num_cols - 1 and wall_tiles[row_index][col_index + 1] != 0:
						mark_tile_right = 1
					elif col_index == self.num_cols - 1:
						mark_tile_right = 2

					# Has tile top left
					if row_index > 0 and col_index > 0 and wall_tiles[row_index - 1][col_index - 1] != 0:
						mark_tile_top_left = 1
					elif row_index == 0 and col_index == 0:
						mark_tile_top_left = 2

					# Has tile top right
					if row_index > 0 and col_index < self.num_cols - 1 and wall_tiles[row_index - 1][col_index + 1] != 0:
						mark_tile_top_right = 1
					elif row_index == 0 and col_index == self.num_cols - 1:
						mark_tile_bottom_right = 2

					# Has tile bottom left
					if row_index < self.num_rows - 1 and col_index > 0 and wall_tiles[row_index + 1][col_index - 1] != 0:
						mark_tile_bottom_left = 1
					elif row_index == self.num_rows - 1 and col_index == 0:
						mark_tile_bottom_left = 2

					# Has tile bottom right
					if row_index < self.num_rows - 1 and col_index < self.num_cols - 1 and wall_tiles[row_index + 1][col_index + 1] != 0:
						mark_tile_bottom_right = 1
					elif row_index == self.num_rows - 1 and col_index == self.num_cols - 1:
						mark_tile_bottom_right = 2

					match (
						mark_tile_top, mark_tile_bottom, mark_tile_left, mark_tile_right,
						mark_tile_top_left, mark_tile_top_right, mark_tile_bottom_left, mark_tile_bottom_right
					):
						# Wall (tile)
						case (1, *remaining) if not (remaining[1] == 0 and remaining[2] == 2) and not (remaining[1] == 2 and remaining[2] == 0) and not (
								remaining[0] == 1 and remaining[3] != 1 and remaining[4] != 1 and remaining[5] != 1 and remaining[6] != 1
						):
							tile_type = 20
						# Wall (air)
						case (0, 0, 1, 1, *_):
							tile_type = 21
						case (0, 0, 1, 0, *_):
							tile_type = 21
						case (0, 0, 0, 1, *_):
							tile_type = 21
						case (0, 0, 0, 0, *_):
							tile_type = 21
						case (0, 1, 1, 1, *_):
							tile_type = 21
						case (0, 1, 1, 0, *_):
							tile_type = 21
						case (0, 1, 0, 1, *_):
							tile_type = 21
						case (0, 1, 0, 0, *_):
							tile_type = 21
						case (0, 2, 1, 1, *_):
							tile_type = 21
						case (0, 2, 1, 0, *_):
							tile_type = 21
						case (0, 2, 0, 1, *_):
							tile_type = 21
						case (0, 2, 0, 0, *_):
							tile_type = 21
						# Wall (void)
						case (2, 0, 1, 1, *_):
							tile_type = 21
						case (2, 0, 1, 0, *_):
							tile_type = 21
						case (2, 0, 0, 1, *_):
							tile_type = 21
						case (2, 0, 0, 0, *_):
							tile_type = 21
						case (2, 1, 1, 1, *_):
							tile_type = 21
						case (2, 1, 1, 0, *_):
							tile_type = 21
						case (2, 1, 0, 1, *_):
							tile_type = 21
						case (2, 1, 0, 0, *_):
							tile_type = 21
						case (2, 2, 1, 1, *_):
							tile_type = 21
						case (2, 2, 1, 0, *_):
							tile_type = 21
						case (2, 2, 0, 1, *_):
							tile_type = 21
						case (2, 2, 0, 0, *_):
							tile_type = 21

						# Top left (tile) Invalid?
						# case (1, 1, 0, 1, *corners):
						# 	tile_type = 22
						# case (1, 1, 2, 1, *corners):
						# 	tile_type = 22
						# case (1, 2, 2, 1, *corners):
						# 	tile_type = 22
						# Top left (void | air)
						case (0, 1, 0, 1, *_):
							tile_type = 23
						case (0, 1, 2, 1, *_):
							tile_type = 23
						case (2, 1, 0, 1, *_):
							tile_type = 23
						case (2, 1, 2, 1, *_):
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
						# Top right (void | air)_
						case (0, 1, 1, 0, *_):
							tile_type = 25
						case (0, 1, 1, 2, *_):
							tile_type = 25
						case (2, 1, 1, 0, *_):
							tile_type = 25
						case (2, 1, 1, 2, *_):
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
						case (1, 1, 2, 0, *_):
							tile_type = 28
						case (1, 2, 0, 0, *corners) if corners[3] == 1:
							tile_type = 28
						case (1, 2, 2, 0, *_):
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

				# print(tile_type, row_index, col_index, (mark_tile_top, mark_tile_bottom, mark_tile_left, mark_tile_right, mark_tile_top_left,
				#                                         mark_tile_top_right, mark_tile_bottom_left, mark_tile_bottom_right))

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

	def draw_layer_with_entities(self, surface: pygame.Surface, camera: pygbase.Camera, layer: int, entities: list):
		# Sort entities
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

	def editor_draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for row in self.tiles[0]:
			for tile in row:
				if tile:
					tile.draw(surface, camera)

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
		for row_index, row in enumerate(self.tiles[1]):
			for col_index, tile in enumerate(row):
				tile_type = 2 if tile is not None else 0
				is_top_wall = True

				if tile_type == 2:
					mark_tile_top = 0
					mark_tile_bottom = 0
					mark_tile_left = 0
					mark_tile_right = 0

					mark_tile_top_left = 0
					mark_tile_top_right = 0
					mark_tile_bottom_left = 0
					mark_tile_bottom_right = 0

					# Has tile on top
					if row_index > 0 and self.tiles[1][row_index - 1][col_index] is not None:
						is_top_wall = False
						mark_tile_top = 1
					elif row_index == 0:
						mark_tile_top = 2

					# Has tile below
					if row_index < self.num_rows - 1 and self.tiles[1][row_index + 1][col_index] is not None:
						mark_tile_bottom = 1
					elif row_index == self.num_rows - 1:
						mark_tile_bottom = 2

					# Has tile to the left
					if col_index > 0 and self.tiles[1][row_index][col_index - 1] is not None:
						mark_tile_left = 1
					elif col_index == 0:
						mark_tile_left = 2

					# Has tile to the right
					if col_index < self.num_cols - 1 and self.tiles[1][row_index][col_index + 1] is not None:
						mark_tile_right = 1
					elif col_index == self.num_cols - 1:
						mark_tile_right = 2

					# Has tile top left
					if row_index > 0 and col_index > 0 and self.tiles[1][row_index - 1][col_index - 1] is not None:
						mark_tile_top_left = 1
					elif row_index == 0 and col_index == 0:
						mark_tile_top_left = 2

					# Has tile top right
					if row_index > 0 and col_index < self.num_cols - 1 and self.tiles[1][row_index - 1][col_index + 1] is not None:
						mark_tile_top_right = 1
					elif row_index == 0 and col_index == self.num_cols - 1:
						mark_tile_bottom_right = 2

					# Has tile bottom left
					if row_index < self.num_rows - 1 and col_index > 0 and self.tiles[1][row_index + 1][col_index - 1] is not None:
						mark_tile_bottom_left = 1
					elif row_index == self.num_rows - 1 and col_index == 0:
						mark_tile_bottom_left = 2

					# Has tile bottom right
					if row_index < self.num_rows - 1 and col_index < self.num_cols - 1 and self.tiles[1][row_index + 1][col_index + 1] is not None:
						mark_tile_bottom_right = 1
					elif row_index == self.num_rows - 1 and col_index == self.num_cols - 1:
						mark_tile_bottom_right = 2

					match (
						mark_tile_top, mark_tile_bottom, mark_tile_left, mark_tile_right,
						mark_tile_top_left, mark_tile_top_right, mark_tile_bottom_left, mark_tile_bottom_right
					):
						# Wall (tile)
						case (1, *remaining) if not (remaining[1] == 0 and remaining[2] == 2) and not (remaining[1] == 2 and remaining[2] == 0) and not (
								remaining[0] == 1 and remaining[3] != 1 and remaining[4] != 1 and remaining[5] != 1 and remaining[6] != 1
						):
							tile_type = 20
						# Wall (air)
						case (0, 0, 1, 1, *_):
							tile_type = 21
						case (0, 0, 1, 0, *_):
							tile_type = 21
						case (0, 0, 0, 1, *_):
							tile_type = 21
						case (0, 0, 0, 0, *_):
							tile_type = 21
						case (0, 1, 1, 1, *_):
							tile_type = 21
						case (0, 1, 1, 0, *_):
							tile_type = 21
						case (0, 1, 0, 1, *_):
							tile_type = 21
						case (0, 1, 0, 0, *_):
							tile_type = 21
						case (0, 2, 1, 1, *_):
							tile_type = 21
						case (0, 2, 1, 0, *_):
							tile_type = 21
						case (0, 2, 0, 1, *_):
							tile_type = 21
						case (0, 2, 0, 0, *_):
							tile_type = 21
						# Wall (void)
						case (2, 0, 1, 1, *_):
							tile_type = 21
						case (2, 0, 1, 0, *_):
							tile_type = 21
						case (2, 0, 0, 1, *_):
							tile_type = 21
						case (2, 0, 0, 0, *_):
							tile_type = 21
						case (2, 1, 1, 1, *_):
							tile_type = 21
						case (2, 1, 1, 0, *_):
							tile_type = 21
						case (2, 1, 0, 1, *_):
							tile_type = 21
						case (2, 1, 0, 0, *_):
							tile_type = 21
						case (2, 2, 1, 1, *_):
							tile_type = 21
						case (2, 2, 1, 0, *_):
							tile_type = 21
						case (2, 2, 0, 1, *_):
							tile_type = 21
						case (2, 2, 0, 0, *_):
							tile_type = 21
						case (0, 1, 0, 1, *_):
							tile_type = 23
						case (0, 1, 2, 1, *_):
							tile_type = 23
						case (2, 1, 0, 1, *_):
							tile_type = 23
						case (2, 1, 2, 1, *_):
							tile_type = 23
						case (1, 1, 0, 1, *corners) if 1 not in corners:
							tile_type = 22
						case (1, 1, 2, 1, *corners) if 1 not in corners:
							tile_type = 22
						case (0, 1, 1, 0, *_):
							tile_type = 25
						case (0, 1, 1, 2, *_):
							tile_type = 25
						case (2, 1, 1, 0, *_):
							tile_type = 25
						case (2, 1, 1, 2, *_):
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
						case (1, 1, 2, 0, *_):
							tile_type = 28
						case (1, 2, 0, 0, *corners) if corners[3] == 1:
							tile_type = 28
						case (1, 2, 2, 0, *_):
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

				if tile_type == 0:
					continue

				if is_top_wall:
					TopWallTile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]).draw(surface, camera)
				else:
					Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]).draw(surface, camera)
