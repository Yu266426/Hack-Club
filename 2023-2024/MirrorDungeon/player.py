import pygame
import pygbase

from consts import TILE_SIZE
from level import Level


class Player:
	def __init__(self, pos: tuple, level: Level):
		self.movement_speed = 500
		self.pos = pygame.Vector2(pos)

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0)
		], "idle")

		self.level = level

	def update(self, delta: float):
		self.animations.update(delta)

		x_input = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.pos.x += x_input * self.movement_speed * delta

		left_tile_pos = self.level.get_tile_pos(self.pos, (-TILE_SIZE / 2, 0))
		right_tile_pos = self.level.get_tile_pos(self.pos, (TILE_SIZE / 2, 0))

		if self.level.check_bounds(left_tile_pos) and self.level.tiles[left_tile_pos[1]][left_tile_pos[0]].collidable:
			self.pos.x = (left_tile_pos[0] + 1) * self.level.TILE_SIZE + TILE_SIZE / 2

		if self.level.check_bounds(right_tile_pos) and self.level.tiles[right_tile_pos[1]][right_tile_pos[0]].collidable:
			self.pos.x = right_tile_pos[0] * self.level.TILE_SIZE - TILE_SIZE / 2

		y_input = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		self.pos.y += y_input * self.movement_speed * delta

		bottom_tile_pos = self.level.get_tile_pos(self.pos)
		top_tile_pos = self.level.get_tile_pos(self.pos, (0, 20 * 5))

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
