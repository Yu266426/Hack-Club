import random

import pygame
import pygbase
from pygbase.resources import json

from consts import TILE_SIZE
from files import LEVELS_DIR
from mirror import HorizontalMirror, VerticalMirror, MirrorType
from mirror_player import TempMirrorPlayer
from tile import Tile, TopWallTile


class Level:
	TILE_MAPPING = {
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

	FLOOR_GEN_MAPPING = {
		"large_crack": 11,
		"medium_crack": 12,
		"bottom_left_hole": 13,
		"small_crack": 14,
		"bottom_right_hole": 15,
		"top_right_hole": 16,
		"top_left_hole": 17
	}

	def __init__(self, name: str, size: tuple[int, int] = (10, 10)):
		self.name = name

		self.TILE_SIZE = 16 * 5

		self.num_rows = size[1]
		self.num_cols = size[0]
		self.tiles: list[list[list[Tile | None]]] = [[], []]  # [Floor, Wall]

		self.horizontal_mirrors: list[HorizontalMirror] = []
		self.vertical_mirrors: list[VerticalMirror] = []

		self.horizontal_mirror_mask_surf = pygame.Surface(pygbase.Common.get_value("screen_size"), flags=pygame.SRCALPHA)
		self.vertical_mirror_mask_surf = pygame.Surface(pygbase.Common.get_value("screen_size"), flags=pygame.SRCALPHA)
		self.horizontal_mirror_mask_tiles = []
		self.vertical_mirror_mask_tiles = []

		self.horizontal_mirror_entity_surf = pygame.Surface(pygbase.Common.get_value("screen_size"), flags=pygame.SRCALPHA)
		self.vertical_mirror_entity_surf = pygame.Surface(pygbase.Common.get_value("screen_size"), flags=pygame.SRCALPHA)

		self.player_spawn_tile_pos: tuple[int, int] = (1, 1)  # Tile pos

		self.load()

		self.process_mirrors()
		print(f"{self.horizontal_mirror_mask_tiles=}")

	def get_colliders(self) -> list[pygame.Rect]:
		colliders = []
		for row in self.tiles[1]:
			for tile in row:
				if tile is None or not tile.collidable:
					continue

				colliders.append(tile.rect)

		return colliders

	def process_mirrors(self):
		for mirror in self.horizontal_mirrors:
			self.horizontal_mirror_mask_tiles.append(mirror.tile_pos)

			for y in reversed(range(0, mirror.tile_pos[1])):
				tile_pos = (mirror.tile_pos[0], y)
				# print(tile_pos)

				self.horizontal_mirror_mask_tiles.append(tile_pos)

				if self.get_tile(tile_pos) is not None:
					break

			for y in range(mirror.tile_pos[1] + 1, self.num_rows):
				tile_pos = (mirror.tile_pos[0], y)
				# print(tile_pos)

				if self.get_tile(tile_pos) is not None:
					break
				self.horizontal_mirror_mask_tiles.append(tile_pos)

		for mirror in self.vertical_mirrors:
			self.vertical_mirror_mask_tiles.append(mirror.tile_pos)

			for x in reversed(range(0, mirror.tile_pos[0])):
				tile_pos = (x, mirror.tile_pos[1])

				self.vertical_mirror_mask_tiles.append(tile_pos)
				if self.get_tile(tile_pos) is not None:
					break

			for x in range(mirror.tile_pos[0] + 1, self.num_cols):
				tile_pos = (x, mirror.tile_pos[1])

				self.vertical_mirror_mask_tiles.append(tile_pos)
				if self.get_tile(tile_pos) is not None:
					break

		for mirror in self.horizontal_mirrors:
			for other_mirror in self.horizontal_mirrors:
				if mirror is not other_mirror:
					if abs(mirror.tile_pos[0] - other_mirror.tile_pos[0]) == 1:
						mirror.adjacent.append(other_mirror)

		for mirror in self.vertical_mirrors:
			for other_mirror in self.vertical_mirrors:
				if mirror is not other_mirror:
					if abs(mirror.tile_pos[1] - other_mirror.tile_pos[1]) == 1:
						mirror.adjacent.append(other_mirror)

		for mirror in self.vertical_mirrors:
			adjacent = [adjacent_mirror.tile_pos for adjacent_mirror in mirror.adjacent]
			print(f"{mirror.tile_pos}: {adjacent}")

	@staticmethod
	def get_tile_pos(pos, offset=(0, 0)) -> tuple[int, int]:
		return int((pos[0] + offset[0]) // TILE_SIZE), int((pos[1] + offset[1]) // TILE_SIZE)

	def get_player_spawn_pos(self) -> tuple[float, float]:
		return self.player_spawn_tile_pos[0] * TILE_SIZE + TILE_SIZE / 2, self.player_spawn_tile_pos[1] * TILE_SIZE + TILE_SIZE

	def check_bounds(self, tile_pos) -> bool:
		return 0 <= tile_pos[0] < self.num_cols and 0 <= tile_pos[1] < self.num_rows

	def get_tile(self, tile_pos, layer=1) -> Tile | None:
		if self.check_bounds(tile_pos):
			return self.tiles[layer][tile_pos[1]][tile_pos[0]]
		else:
			return None

	def load(self):
		file_path = LEVELS_DIR / f"{self.name}.json"
		if not file_path.exists():
			data: dict = {
				"size": [self.num_cols, self.num_rows],
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
				},
				"player_spawn": [1, 1]
			}

			for col in range(self.num_cols):
				data["tiles"]["wall"][0][col] = 2
				data["tiles"]["wall"][self.num_rows - 1][col] = 2

			for row in range(self.num_rows):
				data["tiles"]["wall"][row][0] = 2
				data["tiles"]["wall"][row][self.num_cols - 1] = 2

			self.player_spawn_tile_pos = data["player_spawn"]

			# Create new level file
			with open(file_path, "w") as level_file:
				level_file.write(json.dumps(data))
		else:
			# Load level file
			with open(file_path) as level_file:
				data = json.load(level_file)

			self.num_cols = data["size"][0]
			self.num_rows = data["size"][1]

			self.player_spawn_tile_pos = data["player_spawn"]

			for mirror_data in data["mirrors"]["horizontal"]:
				self.horizontal_mirrors.append(HorizontalMirror(mirror_data["tile_pos"]))

			for mirror_data in data["mirrors"]["vertical"]:
				self.vertical_mirrors.append(VerticalMirror(mirror_data["tile_pos"]))

		floor_tiles: list[list[int]] = data["tiles"]["floor"]
		wall_tiles: list[list[int]] = data["tiles"]["wall"]

		floor_gen_settings = {self.FLOOR_GEN_MAPPING[floor_type]: percentage for floor_type, percentage in data["floor_gen_settings"].items()}

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

				self.tiles[0][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=tile))

		# Wall generation
		for row_index, row in enumerate(wall_tiles):
			self.tiles[1].append([])
			for col_index, tile in enumerate(row):
				if tile == 2:
					is_top_wall, tile_type = self.determine_wall_tile((col_index, row_index), wall_tiles)

					# print(tile_type, row_index, col_index, (mark_tile_top, mark_tile_bottom, mark_tile_left, mark_tile_right, mark_tile_top_left, mark_tile_top_right, mark_tile_bottom_left, mark_tile_bottom_right))
					if is_top_wall:
						self.tiles[1][row_index].append(TopWallTile((col_index * TILE_SIZE, row_index * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=tile))
						continue
					else:
						self.tiles[1][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=tile))
						continue

				if tile == 0:
					self.tiles[1][row_index].append(None)
					continue

				self.tiles[1][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *self.TILE_MAPPING[tile], autogen_value=tile))

	def save(self):
		file_path = LEVELS_DIR / f"{self.name}.json"

		# Load level file
		with open(file_path) as level_file:
			data = json.load(level_file)

		floor_tiles = []
		for row in self.tiles[0]:
			floor_tile_row = []
			for tile in row:
				if tile is not None:
					floor_tile_row.append(tile.autogen_value)
				else:
					floor_tile_row.append(0)
			floor_tiles.append(floor_tile_row)

		wall_tiles = []
		for row in self.tiles[1]:
			wall_tiles_row = []
			for tile in row:
				if tile is not None:
					wall_tiles_row.append(tile.autogen_value)
				else:
					wall_tiles_row.append(0)
			wall_tiles.append(wall_tiles_row)

		data["tiles"]["floor"] = floor_tiles
		data["tiles"]["wall"] = wall_tiles

		data["player_spawn"] = self.player_spawn_tile_pos

		data["mirrors"]["horizontal"] = []
		for mirror in self.horizontal_mirrors:
			data["mirrors"]["horizontal"].append({"tile_pos": mirror.tile_pos})

		data["mirrors"]["vertical"] = []
		for mirror in self.vertical_mirrors:
			data["mirrors"]["vertical"].append({"tile_pos": mirror.tile_pos})

		with open(file_path, "w") as level_file:
			level_file.write(json.dumps(data))

	def determine_wall_tile(self, tile_pos, wall_tiles):
		is_top_wall = True

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
		if tile_pos[1] > 0 and wall_tiles[tile_pos[1] - 1][tile_pos[0]] != 0:
			is_top_wall = False
			mark_tile_top = 1
		elif tile_pos[1] == 0:
			mark_tile_top = 2

		# Has tile below
		if tile_pos[1] < self.num_rows - 1 and wall_tiles[tile_pos[1] + 1][tile_pos[0]] != 0:
			mark_tile_bottom = 1
		elif tile_pos[1] == self.num_rows - 1:
			mark_tile_bottom = 2

		# Has tile to the left
		if tile_pos[0] > 0 and wall_tiles[tile_pos[1]][tile_pos[0] - 1] != 0:
			mark_tile_left = 1
		elif tile_pos[0] == 0:
			mark_tile_left = 2

		# Has tile to the right
		if tile_pos[0] < self.num_cols - 1 and wall_tiles[tile_pos[1]][tile_pos[0] + 1] != 0:
			mark_tile_right = 1
		elif tile_pos[0] == self.num_cols - 1:
			mark_tile_right = 2

		# Has tile top left
		if tile_pos[1] > 0 and tile_pos[0] > 0 and wall_tiles[tile_pos[1] - 1][tile_pos[0] - 1] != 0:
			mark_tile_top_left = 1
		elif tile_pos[1] == 0 and tile_pos[0] == 0:
			mark_tile_top_left = 2

		# Has tile top right
		if tile_pos[1] > 0 and tile_pos[0] < self.num_cols - 1 and wall_tiles[tile_pos[1] - 1][tile_pos[0] + 1] != 0:
			mark_tile_top_right = 1
		elif tile_pos[1] == 0 and tile_pos[0] == self.num_cols - 1:
			mark_tile_bottom_right = 2

		# Has tile bottom left
		if tile_pos[1] < self.num_rows - 1 and tile_pos[0] > 0 and wall_tiles[tile_pos[1] + 1][tile_pos[0] - 1] != 0:
			mark_tile_bottom_left = 1
		elif tile_pos[1] == self.num_rows - 1 and tile_pos[0] == 0:
			mark_tile_bottom_left = 2

		# Has tile bottom right
		if tile_pos[1] < self.num_rows - 1 and tile_pos[0] < self.num_cols - 1 and wall_tiles[tile_pos[1] + 1][tile_pos[0] + 1] != 0:
			mark_tile_bottom_right = 1
		elif tile_pos[1] == self.num_rows - 1 and tile_pos[0] == self.num_cols - 1:
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
			case (1, 1, 1, 1, *remaining):
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
				print(f"Wall at row: {tile_pos[1]} and col: {tile_pos[0]} is not resolved")
				tile_type = 0

		return is_top_wall, tile_type

	def add_wall(self, tile_pos: tuple[int, int]):
		if not self.check_bounds(tile_pos):
			return

		# Convert tiles into wall map
		wall_tiles = []
		for row in self.tiles[1]:
			wall_tiles_row = []
			for tile in row:
				if tile is not None:
					wall_tiles_row.append(tile.autogen_value)
				else:
					wall_tiles_row.append(0)
			wall_tiles.append(wall_tiles_row)

		# Add current wall
		is_top_wall, tile_type = self.determine_wall_tile(tile_pos, wall_tiles)

		if is_top_wall:
			self.tiles[1][tile_pos[1]][tile_pos[0]] = TopWallTile((tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=2)
		else:
			self.tiles[1][tile_pos[1]][tile_pos[0]] = Tile((tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=2)

		# Fix adjacent walls
		wall_tiles = []
		for row in self.tiles[1]:
			wall_tiles_row = []
			for tile in row:
				if tile is not None:
					wall_tiles_row.append(tile.autogen_value)
				else:
					wall_tiles_row.append(0)
			wall_tiles.append(wall_tiles_row)

		adjacent_offsets = [
			(-1, -1),
			(-1, 0),
			(-1, 1),
			(0, -1),
			(0, 1),
			(1, -1),
			(1, 0),
			(1, -1)
		]

		for offset in adjacent_offsets:
			current_tile_pos = tile_pos[0] + offset[0], tile_pos[1] + offset[1]

			if self.check_bounds(current_tile_pos) and wall_tiles[current_tile_pos[1]][current_tile_pos[0]] == 2:
				is_top_wall, tile_type = self.determine_wall_tile(current_tile_pos, wall_tiles)

				if tile_type == 0:
					continue

				if is_top_wall:
					self.tiles[1][current_tile_pos[1]][current_tile_pos[0]] = TopWallTile((current_tile_pos[0] * TILE_SIZE, current_tile_pos[1] * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=2)
				else:
					self.tiles[1][current_tile_pos[1]][current_tile_pos[0]] = Tile((current_tile_pos[0] * TILE_SIZE, current_tile_pos[1] * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=2)

	def remove_wall(self, tile_pos: tuple[int, int]):
		if not (1 <= tile_pos[0] < self.num_cols - 1 and 1 <= tile_pos[1] < self.num_rows - 1):
			return

		# Remove current wall
		self.tiles[1][tile_pos[1]][tile_pos[0]] = None

		# Convert tiles into wall map
		wall_tiles = []
		for row in self.tiles[1]:
			wall_tiles_row = []
			for tile in row:
				if tile is not None:
					wall_tiles_row.append(tile.autogen_value)
				else:
					wall_tiles_row.append(0)
			wall_tiles.append(wall_tiles_row)

		# Fix adjacent walls
		adjacent_offsets = [
			(-1, -1),
			(-1, 0),
			(-1, 1),
			(0, -1),
			(0, 1),
			(1, -1),
			(1, 0),
			(1, -1)
		]

		for offset in adjacent_offsets:
			current_tile_pos = tile_pos[0] + offset[0], tile_pos[1] + offset[1]

			if self.check_bounds(current_tile_pos) and wall_tiles[current_tile_pos[1]][current_tile_pos[0]] == 2:
				is_top_wall, tile_type = self.determine_wall_tile(current_tile_pos, wall_tiles)

				if is_top_wall:
					self.tiles[1][current_tile_pos[1]][current_tile_pos[0]] = TopWallTile((current_tile_pos[0] * TILE_SIZE, current_tile_pos[1] * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=wall_tiles[current_tile_pos[1]][current_tile_pos[0]])
				else:
					self.tiles[1][current_tile_pos[1]][current_tile_pos[0]] = Tile((current_tile_pos[0] * TILE_SIZE, current_tile_pos[1] * TILE_SIZE), *self.TILE_MAPPING[tile_type], autogen_value=wall_tiles[current_tile_pos[1]][current_tile_pos[0]])

	def add_horizontal_mirror(self, tile_pos: tuple[int, int]):
		for mirror in self.horizontal_mirrors:
			if mirror.tile_pos == tile_pos:
				return

		for mirror in self.vertical_mirrors:
			if mirror.tile_pos == tile_pos:
				return

		self.horizontal_mirrors.append(HorizontalMirror(tile_pos))

	def add_vertical_mirror(self, tile_pos: tuple[int, int]):
		for mirror in self.horizontal_mirrors:
			if mirror.tile_pos == tile_pos:
				return

		for mirror in self.vertical_mirrors:
			if mirror.tile_pos == tile_pos:
				return

		self.vertical_mirrors.append(VerticalMirror(tile_pos))

	def remove_mirror(self, tile_pos: tuple[int, int]):
		for mirror in self.horizontal_mirrors[:]:
			if mirror.tile_pos == tile_pos:
				self.horizontal_mirrors.remove(mirror)

		for mirror in self.vertical_mirrors[:]:
			if mirror.tile_pos == tile_pos:
				self.vertical_mirrors.remove(mirror)

	def render_mirror_mask(self, camera: pygbase.Camera):
		# self.mirror_mask_surf.fill((0, 0, 0, 0))
		self.horizontal_mirror_mask_surf.fill((255, 255, 255, 255))
		self.vertical_mirror_mask_surf.fill((255, 255, 255, 255))

		# print(self.horizontal_mirror_mask_tiles)
		for tile in self.horizontal_mirror_mask_tiles:
			pos = tile[0] * TILE_SIZE, tile[1] * TILE_SIZE
			pygame.draw.rect(self.horizontal_mirror_mask_surf, (0, 0, 0, 0), (camera.world_to_screen(pos), (TILE_SIZE, TILE_SIZE)))

		for tile in self.vertical_mirror_mask_tiles:
			pos = tile[0] * TILE_SIZE, tile[1] * TILE_SIZE
			pygame.draw.rect(self.vertical_mirror_mask_surf, (0, 0, 0, 0), (camera.world_to_screen(pos), (TILE_SIZE, TILE_SIZE)))

	def draw_layer(self, surface: pygame.Surface, camera: pygbase.Camera, layer: int):
		for row in self.tiles[layer]:
			for tile in row:
				if tile:
					tile.draw(surface, camera)

	def draw_layer_with_entities(self, surface: pygame.Surface, camera: pygbase.Camera, layer: int, entities: list, mirror_entities: list[TempMirrorPlayer]):
		if len(mirror_entities) != 0:
			self.render_mirror_mask(camera)
			# surface.blit(self.vertical_mirror_mask_surf, (0, 0))

		# Sort entities
		sorted_entities = sorted(entities, key=lambda e: e.pos.y * self.num_cols * self.TILE_SIZE + e.pos.x)
		sorted_mirror_entities = sorted(mirror_entities, key=lambda e: e.from_mirror_type)

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

		mirror_entity_next_index = len(sorted_mirror_entities)
		self.horizontal_mirror_entity_surf.fill((0, 0, 0, 0))
		for index, mirror_entity in enumerate(sorted_mirror_entities):
			if mirror_entity.from_mirror_type == MirrorType.VERTICAL:
				mirror_entity_next_index = index
				break

			mirror_entity.draw(self.horizontal_mirror_entity_surf, camera)
		self.horizontal_mirror_entity_surf.blit(self.horizontal_mirror_mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

		self.vertical_mirror_entity_surf.fill((0, 0, 0, 0))
		for mirror_entity in sorted_mirror_entities[mirror_entity_next_index:]:
			mirror_entity.draw(self.vertical_mirror_entity_surf, camera)
		self.vertical_mirror_entity_surf.blit(self.vertical_mirror_mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

		surface.blit(self.horizontal_mirror_entity_surf, (0, 0))
		surface.blit(self.vertical_mirror_entity_surf, (0, 0))

	def draw_mirrors(self, surface: pygame.Surface, camera: pygbase.Camera):
		for mirror in self.horizontal_mirrors:
			mirror.draw(surface, camera)

		for mirror in self.vertical_mirrors:
			mirror.draw(surface, camera)

	def editor_draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for layer in self.tiles:
			for row in layer:
				for tile in row:
					if tile is not None:
						tile.draw(surface, camera)

		pygame.draw.rect(surface, "blue", (camera.world_to_screen((self.player_spawn_tile_pos[0] * TILE_SIZE, self.player_spawn_tile_pos[1] * TILE_SIZE)), (TILE_SIZE, TILE_SIZE)), width=4)
