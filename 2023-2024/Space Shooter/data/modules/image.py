import os.path

import pygame.image

from data.modules.files import ASSET_DIR


class Image:
	def __init__(self, image_name, angle=0, scale=1):
		self.angle = angle

		self.image = pygame.image.load(os.path.join(ASSET_DIR, f"{image_name}.png")).convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))

	def draw(self, surface: pygame.Surface, pos):
		rotated_image = pygame.transform.rotate(self.image, self.angle)
		image_pos = rotated_image.get_rect(center=self.image.get_rect(center=pos).center)

		surface.blit(rotated_image, image_pos)
