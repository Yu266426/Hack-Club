from typing import Tuple

import pygame.transform

from data.modules.components.image import Image
from data.modules.components.position import Position


class RotatableImage(Image):
	def __init__(self, pos: Position, image: pygame.Surface):
		super().__init__(pos, image)

		self.pos = pos

		self.base_image = self.image.copy()

		self.update_angle()

	@property
	def center_offset(self) -> tuple[float, float]:
		return self.base_image.get_width() / 2, self.base_image.get_height() / 2

	def update_angle(self):
		self.image = pygame.transform.rotate(self.base_image, self.pos.angle)

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		display.blit(self.image, self.image.get_rect(center=self.base_image.get_rect(topleft=self.pos.pos - scroll).center))
