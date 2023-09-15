from pygame import Vector2

from image import Image
from images import LASER_IMAGE


class Laser:
	def __init__(self, pos, angle):
		self.pos = Vector2(pos)

		self.image = Image(LASER_IMAGE, (35, 7), angle)
		self.rect = self.image.get_rect(self.pos)

		self.movement = Vector2(20, 0).rotate(-angle)

	def update(self):
		self.pos += self.movement
		self.rect.center = self.pos

	def draw(self, screen):
		self.image.draw(screen, self.rect)
