from typing import TYPE_CHECKING

import pygame
import pygbase

from consts import PLAYER_HEIGHT, PLAYER_WIDTH

if TYPE_CHECKING:
	from level import Level


class Player:
	def __init__(self, level: "Level"):
		self.movement_speed = 500
		self.movement_speed = 250
		self.pos = pygame.Vector2(level.get_player_spawn_pos())

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0),
			("run", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 8.0)
		], "idle")

		self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
		self.rect.midbottom = self.pos

		self.flip_x = False

		self.level = level
		self.level_colliders = self.level.get_colliders()

	def movement(self, delta: float):
		x_input = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)

		self.pos.x += x_input * self.movement_speed * delta
		self.rect.midbottom = self.pos

		for rect in self.level_colliders:
			if self.rect.colliderect(rect):
				if x_input < 0:
					self.rect.left = rect.right
				elif x_input > 0:
					self.rect.right = rect.left
				self.pos.x = self.rect.centerx

		y_input = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
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
