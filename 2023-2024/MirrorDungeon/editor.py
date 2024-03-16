import logging

import pygame
import pygbase

from consts import TILE_SIZE
from level import Level


class Editor(pygbase.GameState, name="editor"):
	def __init__(self):
		super().__init__()

		self.level: Level = Level(pygbase.Common.get_value("level_name"), size=pygbase.Common.get_value("level_size"))

		self.camera_controller = pygbase.CameraController(keep_in=(-200, -200, self.level.num_cols * TILE_SIZE + 200, self.level.num_rows * TILE_SIZE + 200))

	def update(self, delta: float):
		if pygbase.InputManager.check_modifiers(pygame.KMOD_CTRL) or pygbase.InputManager.check_modifiers(pygame.KMOD_META):
			if pygbase.InputManager.get_key_just_pressed(pygame.K_s):
				logging.info(f"Saving level: {self.level.name}")
				self.level.save()
			return

		self.camera_controller.update(delta)

		tile_pos = self.level.get_tile_pos(self.camera_controller.camera.screen_to_world(pygame.mouse.get_pos()))

		if pygbase.InputManager.get_mouse_pressed(0):
			self.level.add_wall(tile_pos)

		elif pygbase.InputManager.get_mouse_pressed(2):
			self.level.remove_wall(tile_pos)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_SPACE):
			self.level.player_spawn_tile_pos = tile_pos

	def draw(self, surface: pygame.Surface):
		surface.fill("black")

		self.level.editor_draw(surface, self.camera_controller.camera)
