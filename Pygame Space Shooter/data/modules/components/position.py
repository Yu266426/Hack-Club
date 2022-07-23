import pygame


class Position:
	def __init__(self, pos: tuple[int, int] | pygame.Vector2, radius: int, angle: float = 0):
		self.pos = pygame.Vector2(pos)

		self.angle = angle

		self._center_offset = None

		self.radius = radius

	def generate_center(self, center_offset: tuple[int | float, int | float]):
		self._center_offset = center_offset

	def center_self(self):
		self.pos -= self._center_offset

	@property
	def center(self) -> tuple[int, int] | pygame.Vector2:
		if self._center_offset is not None:
			return self.pos + self._center_offset
		else:
			return self.pos

	def copy(self) -> "Position":
		return Position(self.pos, self.angle)

	def move_with_vector(self, vector: pygame.Vector2):
		self.pos += vector
