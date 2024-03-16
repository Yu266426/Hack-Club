import pygame
import pygbase

from consts import PLAYER_HEIGHT, TILE_SIZE, PLAYER_WIDTH
from level import Level


class Player:
	def __init__(self, level: Level):
		self.movement_speed = 500
		self.movement_speed = 250
		self.pos = pygame.Vector2(level.get_player_spawn_pos())

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0),
			("run", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 8.0)
		], "idle"
		)
		self.flip_x = False

		self.level = level

	def update(self, delta: float):
		self.animations.update(delta)

		x_input = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.pos.x += x_input * self.movement_speed * delta

		if x_input < 0:
			for y_offset in range(1, PLAYER_HEIGHT - 1, TILE_SIZE):
				left_tile_pos = self.level.get_tile_pos(self.pos, (-int(PLAYER_WIDTH / 2), -y_offset))

				tile = self.level.get_tile(left_tile_pos)

				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (-int(PLAYER_WIDTH / 2), -y_offset)):
					self.pos.x = left_tile_pos[0] * TILE_SIZE + tile.rect.width + PLAYER_WIDTH / 2

			if PLAYER_HEIGHT % TILE_SIZE != 0:
				left_tile_pos = self.level.get_tile_pos(self.pos, (-int(PLAYER_WIDTH / 2), -PLAYER_HEIGHT + 1))

				tile = self.level.get_tile(left_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (-int(PLAYER_WIDTH / 2), -PLAYER_HEIGHT + 1)):
					self.pos.x = left_tile_pos[0] * TILE_SIZE + tile.rect.width + PLAYER_WIDTH / 2

		if x_input > 0:
			for y_offset in range(1, PLAYER_HEIGHT - 1, TILE_SIZE):
				right_tile_pos = self.level.get_tile_pos(self.pos, (int(PLAYER_WIDTH / 2), -y_offset))

				tile = self.level.get_tile(right_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (int(PLAYER_WIDTH / 2), -y_offset)):
					self.pos.x = (right_tile_pos[0] + 1) * TILE_SIZE - tile.rect.width - PLAYER_WIDTH / 2

			if PLAYER_HEIGHT % TILE_SIZE != 0:
				right_tile_pos = self.level.get_tile_pos(self.pos, (int(PLAYER_WIDTH / 2), -PLAYER_HEIGHT + 1))

				tile = self.level.get_tile(right_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (int(PLAYER_WIDTH / 2), -PLAYER_HEIGHT + 1)):
					self.pos.x = (right_tile_pos[0] + 1) * TILE_SIZE - tile.rect.width - PLAYER_WIDTH / 2

		y_input = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		self.pos.y += y_input * self.movement_speed * delta

		if y_input < 0:
			for x_offset in range(int(-PLAYER_WIDTH / 2) + 1, int(PLAYER_WIDTH / 2) - 1, TILE_SIZE):
				top_tile_pos = self.level.get_tile_pos(self.pos, (x_offset, -PLAYER_HEIGHT))

				tile = self.level.get_tile(top_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (x_offset, -PLAYER_HEIGHT)):
					self.pos.y = top_tile_pos[1] * TILE_SIZE + tile.rect.height + PLAYER_HEIGHT

			if PLAYER_WIDTH % TILE_SIZE != 0:
				top_tile_pos = self.level.get_tile_pos(self.pos, (int(PLAYER_WIDTH / 2) - 1, -PLAYER_HEIGHT))

				tile = self.level.get_tile(top_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (int(PLAYER_WIDTH / 2) - 1, -PLAYER_HEIGHT)):
					self.pos.y = top_tile_pos[1] * TILE_SIZE + tile.rect.height + PLAYER_HEIGHT

		if y_input > 0:
			for x_offset in range(int(-PLAYER_WIDTH / 2) + 1, int(PLAYER_WIDTH / 2) - 1, TILE_SIZE):
				bottom_tile_pos = self.level.get_tile_pos(self.pos, (x_offset, 0))

				tile = self.level.get_tile(bottom_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (x_offset, 0)):
					self.pos.y = (bottom_tile_pos[1] + 1) * TILE_SIZE - tile.rect.height

			if PLAYER_WIDTH % TILE_SIZE != 0:
				bottom_tile_pos = self.level.get_tile_pos(self.pos, (int(PLAYER_WIDTH / 2) - 1, 0))

				tile = self.level.get_tile(bottom_tile_pos)
				if tile is not None and tile.collidable and tile.rect.collidepoint(self.pos + (int(PLAYER_WIDTH / 2) - 1, 0)):
					self.pos.y = (bottom_tile_pos[1] + 1) * TILE_SIZE - tile.rect.height

		if x_input != 0 or y_input != 0:
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

		if x_input < 0:
			self.flip_x = True
		elif x_input > 0:
			self.flip_x = False

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom", flip=(self.flip_x, False))
