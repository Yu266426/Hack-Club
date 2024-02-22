import pygame
import pygbase
import random

from consts import TILE_SIZE
from tile import Tile, TopWallTile


class Level:
	def __init__(self):
		self.TILE_SIZE = 16 * 5

		self.num_rows = 0
		self.num_cols = 0
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
		    21: ("wall_tiles", 6, True, 0),
		    22: ("wall_tiles", 0, True, 1),  # Top left
		    23: ("wall_tiles", 1, True, 2),  # Top right
		    24: ("wall_tiles", 2, True),  # Left
		    25: ("wall_tiles", 3, True),  # Right
		    26: ("wall_tiles", 4, True),  # Bottom left
		    27: ("wall_tiles", 5, True),  # Bottom right
		    28: ("wall_alternates", 0, True),
		    29: ("wall_alternates", 1, True),
		    210: ("wall_alternates", 3, True)
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
		  [2, 0, 2, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 0, 0, 0, 0, 0, 2, 2, 0, 2],
		  [2, 2, 0, 0, 0, 0, 0, 0, 0, 2],
		  [2, 2, 2, 0, 0, 0, 0, 0, 0, 2],
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
				is_top_wall = False

				if tile == 2:
					tile_type = 20

					# TODO: Redo this using a strategy of
					# marking adjacent tiles, then computing the wall type
					#
					# Potentially even precompute an adjacency map, then in the next pass compute tile type
					mark_left_wall = 0
					mark_right_wall = 0

					has_below = False

					# Wall is on top
					if row_index <= 0 or temp_map[1][row_index - 1][col_index] == 0:
						is_top_wall = True

					# Is left wall
					if col_index <= 0:
						mark_left_wall = 1  # Against edge of map
					elif temp_map[1][row_index][col_index - 1] == 0:
						mark_left_wall = 2  # No tile on left

					# Is right wall
					if col_index >= self.num_cols - 1:
						mark_right_wall = 1  # Against edge of map
					elif temp_map[1][row_index][col_index + 1] == 0:
						mark_right_wall = 2  # No tile on right

					# Has below
					if row_index < self.num_rows - 1 and temp_map[1][row_index + 1][col_index]:
						has_below = True

					# Compute wall type
					if is_top_wall:
						tile_type = 21

					if has_below:
						if is_top_wall:
							if mark_left_wall == 1 or (mark_left_wall == 2 and mark_right_wall == 0):
								tile_type = 22
							if mark_right_wall == 1 or (mark_right_wall == 2 and mark_left_wall == 0):
								tile_type = 23
						else:
							if mark_left_wall != 0 and mark_right_wall == 2:
								tile_type = 24
							if mark_right_wall != 0 and mark_left_wall == 2:
								tile_type = 25

				print(tile_type, row_index, col_index)
				if is_top_wall:
					self.tiles[1][row_index].append(TopWallTile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]))
				else:
					self.tiles[1][row_index].append(Tile((col_index * TILE_SIZE, row_index * TILE_SIZE), *tile_mapping[tile_type]))

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
			for tile in row:
				if tile:
					tile.draw(surface, camera)

			for entity in sorted_entities[current_entity_index:]:
				if self.get_tile_pos(entity.pos)[1] != row_index:
					break

				entity.draw(surface, camera)

				current_entity_index += 1

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		for layer in self.tiles:
			for row in layer:
				for tile in row:
					if tile:
						tile.draw(surface, camera)
