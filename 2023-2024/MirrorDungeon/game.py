from collections import deque

import pygame
import pygbase

from consts import TILE_SIZE
from level import Level
from mirror import MirrorType, Mirror
from mirror_player import TempMirrorPlayer, MirrorPlayer
from player import Player


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()

		self.camera = pygbase.Camera()
		pygbase.Common.set_value("camera", self.camera)

		self.level = Level(pygbase.Common.get_value("level_name"))

		self.player = Player(self.level)
		self.temp_mirror_players: list[TempMirrorPlayer] = []
		self.mirror_enemies: list = []

		self.currently_mirroring: set[Mirror] = set()

	def update(self, delta: float):
		# print(len(self.mirror_players))
		# print(self.currently_mirroring)

		self.player.update(delta)

		adjacent_mirror_queue = deque()
		for mirror in self.level.horizontal_mirrors:
			if mirror in self.currently_mirroring:
				continue

			if mirror.pos.x < self.player.rect.right and self.player.rect.left < mirror.pos.x + TILE_SIZE:
				self.temp_mirror_players.append(TempMirrorPlayer(self.player, MirrorType.HORIZONTAL, mirror))
				self.currently_mirroring.add(mirror)
				adjacent_mirror_queue.extend([adjacent for adjacent in mirror.adjacent if adjacent not in self.currently_mirroring])

				while len(adjacent_mirror_queue) > 0:
					adjacent_mirror = adjacent_mirror_queue.popleft()
					adjacent_mirror_queue.extend([adjacent for adjacent in adjacent_mirror.adjacent if adjacent not in self.currently_mirroring])

					self.currently_mirroring.add(adjacent_mirror)
		adjacent_mirror_queue.clear()

		for mirror in self.player.level.vertical_mirrors:
			if mirror in self.currently_mirroring:
				continue

			if mirror.pos.y < self.player.rect.bottom and self.player.rect.top < mirror.pos.y + TILE_SIZE:
				self.temp_mirror_players.append(TempMirrorPlayer(self.player, MirrorType.VERTICAL, mirror))

				self.currently_mirroring.add(mirror)
				adjacent_mirror_queue.extend([adjacent for adjacent in mirror.adjacent if adjacent not in self.currently_mirroring])

				while len(adjacent_mirror_queue) > 0:
					adjacent_mirror = adjacent_mirror_queue.popleft()
					adjacent_mirror_queue.extend([adjacent for adjacent in adjacent_mirror.adjacent if adjacent not in self.currently_mirroring])

					self.currently_mirroring.add(adjacent_mirror)
		adjacent_mirror_queue.clear()

		for mirror_player in self.temp_mirror_players:
			if mirror_player.update(delta):
				self.mirror_enemies.append(MirrorPlayer(mirror_player.get_mirror_pos(), self.level, mirror_player.get_mirror_flip_x(), self.player))

			if not mirror_player.in_mirror:
				self.currently_mirroring.remove(mirror_player.from_mirror)
				adjacent_mirror_queue.extend([adjacent for adjacent in mirror_player.from_mirror.adjacent if adjacent in self.currently_mirroring])

				while len(adjacent_mirror_queue) > 0:
					adjacent_mirror = adjacent_mirror_queue.popleft()
					adjacent_mirror_queue.extend([adjacent for adjacent in adjacent_mirror.adjacent if adjacent in self.currently_mirroring])

					self.currently_mirroring.remove(adjacent_mirror)
		adjacent_mirror_queue.clear()

		self.temp_mirror_players[:] = [mirror_player for mirror_player in self.temp_mirror_players if mirror_player.in_mirror]

		for mirror_enemy in self.mirror_enemies:
			mirror_enemy.update(delta)

		self.camera.lerp_to_target(self.player.pos - pygame.Vector2(400, 400), 1.3 * delta)

	def draw(self, surface: pygame.Surface):
		surface.fill("black")
		self.level.draw_layer(surface, self.camera, 0)
		self.level.draw_layer_with_entities(surface, self.camera, 1, [self.player, *self.mirror_enemies], [*self.temp_mirror_players])
		self.level.draw_mirrors(surface, self.camera)

# pygame.draw.rect(surface, "white",pygame.Rect(self.camera.world_to_screen((self.player.pos.x - PLAYER_WIDTH / 2, self.player.pos.y - PLAYER_HEIGHT)), (PLAYER_WIDTH, PLAYER_HEIGHT)))
