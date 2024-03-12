import pygame
import pygbase

from consts import TILE_SIZE
from level import Level


class Editor(pygbase.GameState, name="editor"):
	def __init__(self):
		super().__init__()

		self.level: Level = Level(pygbase.Common.get_value("level_name"))

		self.camera_controller = pygbase.CameraController(keep_in=(-200, -200, self.level.num_cols * TILE_SIZE + 200, self.level.num_rows * TILE_SIZE + 200))

	def update(self, delta: float):
		self.camera_controller.update(delta)

	def draw(self, surface: pygame.Surface):
		surface.fill("black")

		self.level.editor_draw(surface, self.camera_controller.camera)
