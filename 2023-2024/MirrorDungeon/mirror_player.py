import enum
import random
from typing import TYPE_CHECKING

import pygame
import pygbase

from consts import TILE_SIZE, PLAYER_WIDTH, PLAYER_HEIGHT
from player import Player
from mirror import MirrorType, Mirror

if TYPE_CHECKING:
	from level import Level


class TempMirrorPlayer:
	def __init__(self, player: Player, from_mirror_type: MirrorType, from_mirror: "Mirror"):
		self.player = player
		self.from_mirror_type = from_mirror_type
		self.from_mirror = from_mirror

		self.in_mirror = True
		self.has_spawned = False

		self.pos = self.player.pos

		self.spawn_timer = pygbase.Timer(1.5, False, False)

	def get_mirror_pos(self):
		match self.from_mirror_type:
			case MirrorType.HORIZONTAL:
				return self.player.pos + pygame.Vector2(0, self.from_mirror.pos.y + TILE_SIZE - self.player.pos.y) * 2

			case MirrorType.VERTICAL:
				return self.player.pos + pygame.Vector2(self.from_mirror.pos.x + TILE_SIZE / 2 - self.player.pos.x, 0) * 2

	def get_mirror_flip_x(self):
		match self.from_mirror_type:
			case MirrorType.HORIZONTAL:
				return self.player.flip_x

			case MirrorType.VERTICAL:
				return not self.player.flip_x

	def update(self, delta: float):
		self.spawn_timer.tick(delta)

		self.pos = self.player.pos

		match self.from_mirror_type:
			case MirrorType.HORIZONTAL:
				self.in_mirror = False

				for mirror in self.player.level.horizontal_mirrors:
					if mirror.pos.x < self.player.rect.right and self.player.rect.left < mirror.pos.x + TILE_SIZE:
						self.in_mirror = True

			case MirrorType.VERTICAL:
				self.in_mirror = False

				for mirror in self.player.level.vertical_mirrors:
					if mirror.pos.y < self.player.rect.bottom and self.player.rect.top < mirror.pos.y + TILE_SIZE:
						self.in_mirror = True

		if not self.has_spawned and self.spawn_timer.done():
			self.has_spawned = True
			return True

		return False

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		if not self.has_spawned:
			match self.from_mirror_type:
				case MirrorType.HORIZONTAL:
					self.player.animations.draw_at_pos(
						surface,
						self.player.pos + pygame.Vector2(0, self.from_mirror.pos.y + TILE_SIZE - self.player.pos.y) * 2,
						camera, draw_pos="midbottom", flip=(self.player.flip_x, False)
					)

				case MirrorType.VERTICAL:
					self.player.animations.draw_at_pos(
						surface,
						self.player.pos + pygame.Vector2(self.from_mirror.pos.x + TILE_SIZE / 2 - self.player.pos.x, 0) * 2,
						camera, draw_pos="midbottom", flip=(not self.player.flip_x, False)
					)


class MirrorPlayerState(enum.Enum):
	IDLE = enum.auto()
	WANDER = enum.auto()
	ATTACK = enum.auto()


class WanderState:
	def __init__(self, tile_pos: tuple):
		self.target_tile = tile_pos
		self.target_pos = self.target_tile[0] * TILE_SIZE, self.target_tile[1] * TILE_SIZE


class MirrorPlayerAI:
	def __init__(self, parent: "MirrorPlayer", level: "Level"):
		self.parent = parent

		self.state = MirrorPlayerState.IDLE
		self.time_since_switch = 0

		self.level = level

		self.current_state_info = None

	def switch_state(self, state: MirrorPlayerState):
		if self.state != state:
			self.state = state
			self.time_since_switch = 0

			self.current_state_info = None

	def update(self, delta: float, player: Player):
		self.time_since_switch += delta

		movement = pygame.Vector2(0, 0)

		match self.state:
			case MirrorPlayerState.IDLE:
				if self.time_since_switch > 1.5:
					self.switch_state(MirrorPlayerState.WANDER)
			case MirrorPlayerState.WANDER:
				if self.current_state_info is None:
					target_tile = (
						random.randrange(0, self.level.num_cols),
						random.randrange(0, self.level.num_rows)
					)

					self.current_state_info = WanderState(target_tile)

				movement.update(self.current_state_info.target_pos - self.parent.pos)
				if movement.length() > 5:
					movement.normalize_ip()
				else:
					movement.update(0, 0)

				if self.time_since_switch > 2:
					self.switch_state(MirrorPlayerState.IDLE)

		return movement


class MirrorPlayer:
	def __init__(self, pos: tuple, level: "Level", flip_x: bool, player: Player):
		self.movement_speed = 500
		self.movement_speed = 250
		self.pos = pygame.Vector2(pos)

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0),
			("run", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 8.0)
		], "idle")

		self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
		self.rect.midbottom = self.pos

		self.flip_x = flip_x

		self.level = level
		self.level_colliders = self.level.get_colliders()

		self.player: Player = player
		self.ai = MirrorPlayerAI(self, self.level)

	def movement(self, delta: float):
		target_movement = self.ai.update(delta, self.player)

		x_input = target_movement.x

		self.pos.x += x_input * self.movement_speed * delta
		self.rect.midbottom = self.pos

		for rect in self.level_colliders:
			if self.rect.colliderect(rect):
				if x_input < 0:
					self.rect.left = rect.right
				elif x_input > 0:
					self.rect.right = rect.left
				self.pos.x = self.rect.centerx

		y_input = target_movement.y
		self.pos.y += y_input * self.movement_speed * delta
		self.rect.midbottom = self.pos

		for rect in self.level_colliders:
			if self.rect.colliderect(rect):
				if y_input < 0:
					self.rect.top = rect.bottom
				elif y_input > 0:
					self.rect.bottom = rect.top
				self.pos.y = self.rect.bottom

		if x_input != 0 or y_input != 0:
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

		if x_input < 0:
			self.flip_x = True
		elif x_input > 0:
			self.flip_x = False

	def update(self, delta: float):
		self.animations.update(delta)

		self.movement(delta)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom", flip=(self.flip_x, False))

		pygame.draw.circle(surface, "yellow", camera.world_to_screen(self.pos), 5)
