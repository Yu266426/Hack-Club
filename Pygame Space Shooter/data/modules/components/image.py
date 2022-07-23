import pygame

from data.modules.components.position import Position


class Image:
	def __init__(self, pos: Position, image: pygame.Surface, colour=None):
		self.pos = pos

		self.image = image
		if colour is not None:
			self.image.fill(colour)

	@property
	def center_offset(self) -> tuple[float, float]:
		return self.image.get_width() / 2, self.image.get_height() / 2

	def scale_image(self, new_size: tuple[int, int]) -> None:
		self.image = pygame.transform.scale(self.image, new_size)

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		display.blit(self.image, self.pos.pos - scroll)
