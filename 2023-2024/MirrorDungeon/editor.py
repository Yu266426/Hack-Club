import enum
import logging

import pygame
import pygbase

from consts import TILE_SIZE
from level import Level


class EditorModes(enum.StrEnum):
	TILE = "tile"
	MIRROR = "mirror"
	PLAYER = "player"


class Editor(pygbase.GameState, name="editor"):
	def __init__(self):
		super().__init__()

		self.level: Level = Level(pygbase.Common.get_value("level_name"), size=pygbase.Common.get_value("level_size"))

		self.camera_controller = pygbase.CameraController(keep_in=(-200, -200, self.level.num_cols * TILE_SIZE + 200, self.level.num_rows * TILE_SIZE + 200))

		self.editor_modes = list(EditorModes)
		print(self.editor_modes)
		self.current_mode_index = 0
		self.current_mode = self.editor_modes[self.current_mode_index]

		self.ui = pygbase.UIManager()
		self.left_button = self.ui.add_element(pygbase.Button(
			(pygbase.UIValue(20), pygbase.UIValue(20)),
			(pygbase.UIValue(80), pygbase.UIValue(80)),
			"images", "left_button",
			self.ui.base_container,
			self.left_button_pressed
		))

		self.right_button = self.ui.add_element(pygbase.Button(
			(pygbase.UIValue(20), pygbase.UIValue(20)),
			(pygbase.UIValue(80), pygbase.UIValue(80)),
			"images", "right_button",
			self.ui.base_container,
			self.right_button_pressed
		), align_with_previous=(False, True), add_on_to_previous=(True, False))

		print(pygbase.Common.get_value("screen_width") - 20)
		self.text = self.ui.add_element(pygbase.TextElement(
			(pygbase.UIValue(pygbase.Common.get_value("screen_width") - 20), pygbase.UIValue(20)),
			"arial",
			pygbase.UIValue(50), "white", self.current_mode,
			self.ui.base_container,
			alignment=pygbase.UIAlignment.TOP_RIGHT
		))

	def left_button_pressed(self):
		self.current_mode_index += -1
		self.current_mode_index %= len(self.editor_modes)

		self.current_mode = self.editor_modes[self.current_mode_index]
		self.text.set_text(self.current_mode)

	def right_button_pressed(self):
		self.current_mode_index += 1
		self.current_mode_index %= len(self.editor_modes)

		self.current_mode = self.editor_modes[self.current_mode_index]
		self.text.set_text(self.current_mode)

	def update(self, delta: float):
		# Save level
		if pygbase.InputManager.check_modifiers(pygame.KMOD_CTRL) or pygbase.InputManager.check_modifiers(pygame.KMOD_META):
			if pygbase.InputManager.get_key_just_pressed(pygame.K_s):
				logging.info(f"Saving level: {self.level.name}")
				self.level.save()
			return

		self.ui.update(delta)
		self.camera_controller.update(delta)

		tile_pos = self.level.get_tile_pos(self.camera_controller.camera.screen_to_world(pygame.mouse.get_pos()))

		# Editing
		if not self.ui.on_ui():
			# Tile mode
			if self.current_mode == EditorModes.TILE:
				if pygbase.InputManager.get_mouse_pressed(0):
					self.level.add_wall(tile_pos)

				elif pygbase.InputManager.get_mouse_pressed(2):
					self.level.remove_wall(tile_pos)

			elif self.current_mode == EditorModes.MIRROR:
				pass

			elif self.current_mode == EditorModes.PLAYER:
				if self.level.get_tile(tile_pos) is None and pygbase.InputManager.get_mouse_pressed(0):
					self.level.player_spawn_tile_pos = tile_pos

	def draw(self, surface: pygame.Surface):
		surface.fill("black")

		self.level.editor_draw(surface, self.camera_controller.camera)

		tile_pos = self.level.get_tile_pos(self.camera_controller.camera.screen_to_world(pygame.mouse.get_pos()))

		match self.current_mode:
			case EditorModes.TILE:
				is_deleting = pygbase.InputManager.get_mouse_pressed(2)
				pygame.draw.rect(surface, "red" if is_deleting else "light blue", (
					self.camera_controller.camera.world_to_screen((tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE)), (TILE_SIZE, TILE_SIZE)
				), width=2)
			case EditorModes.MIRROR:
				pass
			case EditorModes.PLAYER:
				is_valid_pos = self.level.get_tile(tile_pos) is None

				pygame.draw.rect(surface, "light blue" if is_valid_pos else "red", (
					self.camera_controller.camera.world_to_screen((tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE)), (TILE_SIZE, TILE_SIZE)
				), width=2)
			case _:
				pass

		self.ui.draw(surface)
