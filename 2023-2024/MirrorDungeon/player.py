import pygame
import pygbase

from consts import PLAYER_HEIGHT, TILE_SIZE, PLAYER_WIDTH
from level import Level


class Player:
	def __init__(self, pos: tuple, level: Level):
		self.movement_speed = 500
		self.movement_speed = 250
		self.pos = pygame.Vector2(pos)

		self.animations = pygbase.AnimationManager([("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0),
		                                            ("run", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 8.0)], "idle")

		self.level = level

	def update(self, delta: float):
		self.animations.update(delta)

		x_input = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.pos.x += x_input * self.movement_speed * delta

		if x_input < 0:
			for y_offset in range(0, PLAYER_HEIGHT, TILE_SIZE):
				left_tile_pos = self.level.get_tile_pos(self.pos, (-PLAYER_WIDTH / 2, -y_offset))
				if self.level.check_tile_collidable(left_tile_pos):
					self.pos.x = (left_tile_pos[0] + 1) * TILE_SIZE + PLAYER_WIDTH / 2

			if PLAYER_HEIGHT % TILE_SIZE != 0:
				left_tile_pos = self.level.get_tile_pos(self.pos, (-PLAYER_WIDTH / 2, -PLAYER_HEIGHT))
				if self.level.check_tile_collidable(left_tile_pos):
					self.pos.x = (left_tile_pos[0] + 1) * TILE_SIZE + PLAYER_WIDTH / 2

		if x_input > 0:
			for y_offset in range(0, PLAYER_HEIGHT, TILE_SIZE):
				right_tile_pos = self.level.get_tile_pos(self.pos, (PLAYER_WIDTH / 2, -y_offset))
				if self.level.check_tile_collidable(right_tile_pos):
					self.pos.x = (right_tile_pos[0]) * TILE_SIZE - PLAYER_WIDTH / 2

			if PLAYER_HEIGHT % TILE_SIZE != 0:
				right_tile_pos = self.level.get_tile_pos(self.pos, (PLAYER_WIDTH / 2, -PLAYER_HEIGHT))
				if self.level.check_tile_collidable(right_tile_pos):
					self.pos.x = (right_tile_pos[0]) * TILE_SIZE - PLAYER_WIDTH / 2

		y_input = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		self.pos.y += y_input * self.movement_speed * delta

		bottom_tile_pos = self.level.get_tile_pos(self.pos)
		top_tile_pos = self.level.get_tile_pos(self.pos, (0, 20 * 5))
		if y_input < 0:
			for x_offset in range(int(-PLAYER_WIDTH / 2), int(PLAYER_WIDTH / 2), TILE_SIZE):
				top_tile_pos = self.level.get_tile_pos(self.pos, (x_offset, -PLAYER_HEIGHT))
				if self.level.check_tile_collidable(top_tile_pos):
					self.pos.y = (top_tile_pos[1] + 1) * TILE_SIZE + PLAYER_HEIGHT

			if PLAYER_WIDTH % TILE_SIZE != 0:
				top_tile_pos = self.level.get_tile_pos(self.pos, (int(PLAYER_WIDTH / 2), -PLAYER_HEIGHT))
				if self.level.check_tile_collidable(top_tile_pos):
					self.pos.y = (top_tile_pos[1] + 1) * TILE_SIZE + PLAYER_HEIGHT

		if y_input > 0:
			for x_offset in range(int(-PLAYER_WIDTH / 2), int(PLAYER_WIDTH / 2), TILE_SIZE):
				bottom_tile_pos = self.level.get_tile_pos(self.pos, (x_offset, 0))
				if self.level.check_tile_collidable(bottom_tile_pos):
					self.pos.y = bottom_tile_pos[1] * TILE_SIZE - 1

			if PLAYER_WIDTH % TILE_SIZE != 0:
				bottom_tile_pos = self.level.get_tile_pos(self.pos, (int(PLAYER_WIDTH / 2), 0))
				if self.level.check_tile_collidable(bottom_tile_pos):
					self.pos.y = bottom_tile_pos[1] * TILE_SIZE - 1

		if x_input != 0 or y_input != 0:
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
