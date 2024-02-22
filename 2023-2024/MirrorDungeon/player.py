import pygame
import pygbase

<<<<<<< Updated upstream
from consts import TILE_SIZE
=======
from consts import PLAYER_HEIGHT, TILE_SIZE, PLAYER_WIDTH
>>>>>>> Stashed changes
from level import Level


class Player:
	def __init__(self, pos: tuple, level: Level):
<<<<<<< Updated upstream
		self.movement_speed = 500
=======
		self.movement_speed = 250
>>>>>>> Stashed changes
		self.pos = pygame.Vector2(pos)

		self.animations = pygbase.AnimationManager([("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0),
		                                            ("run", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 8.0)], "idle")

		self.level = level

		self.level = level

	def update(self, delta: float):
		self.animations.update(delta)

		x_input = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.pos.x += x_input * self.movement_speed * delta

<<<<<<< Updated upstream
		left_tile_pos = self.level.get_tile_pos(self.pos, (-TILE_SIZE / 2, 0))
		right_tile_pos = self.level.get_tile_pos(self.pos, (TILE_SIZE / 2, 0))

		if self.level.check_bounds(left_tile_pos) and self.level.tiles[left_tile_pos[1]][left_tile_pos[0]].collidable:
			self.pos.x = (left_tile_pos[0] + 1) * self.level.TILE_SIZE + TILE_SIZE / 2

		if self.level.check_bounds(right_tile_pos) and self.level.tiles[right_tile_pos[1]][right_tile_pos[0]].collidable:
			self.pos.x = right_tile_pos[0] * self.level.TILE_SIZE - TILE_SIZE / 2
=======
		if x_input < 0:
			left_tile_pos = self.level.get_tile_pos(self.pos, (-PLAYER_WIDTH / 2, 0))
			if self.level.check_tile_collidable(left_tile_pos):
				self.pos.x = (left_tile_pos[0] + 1) * TILE_SIZE + PLAYER_WIDTH / 2

		if x_input > 0:
			right_tile_pos = self.level.get_tile_pos(self.pos, (PLAYER_WIDTH / 2, 0))
			if self.level.check_tile_collidable(right_tile_pos):
				self.pos.x = (right_tile_pos[0]) * TILE_SIZE - PLAYER_WIDTH / 2
>>>>>>> Stashed changes

		y_input = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		self.pos.y += y_input * self.movement_speed * delta

<<<<<<< Updated upstream
		bottom_tile_pos = self.level.get_tile_pos(self.pos)
		top_tile_pos = self.level.get_tile_pos(self.pos, (0, 20 * 5))
=======
		if y_input < 0:
			top_tile_pos = self.level.get_tile_pos(self.pos, (0, -PLAYER_HEIGHT))
			if self.level.check_tile_collidable(top_tile_pos):
				self.pos.y = (top_tile_pos[1] + 1) * TILE_SIZE + PLAYER_HEIGHT

		if y_input > 0:
			bottom_tile_pos = self.level.get_tile_pos(self.pos)
			if self.level.check_tile_collidable(bottom_tile_pos):
				self.pos.y = bottom_tile_pos[1] * TILE_SIZE - 1

		if x_input != 0 or y_input != 0:
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")
>>>>>>> Stashed changes

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
