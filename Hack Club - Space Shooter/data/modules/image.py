import os

import pygame

from data.modules.file import ASSET_DIR


class Image:
	def __init__(self, name, scale, angle):
		self.angle = angle

		self.base_image = pygame.image.load(os.path.join(ASSET_DIR, f"{name}.png"))
		self.base_image = pygame.transform.scale(self.base_image, (self.base_image.get_width() * scale, self.base_image.get_height() * scale))
		self.image = pygame.transform.rotate(self.base_image, self.angle)

	def update_angle(self, new_angle):
		self.angle = new_angle
		self.image = pygame.transform.rotate(self.base_image, self.angle)

	def get_rect(self, pos):
		return self.base_image.get_rect(center=pos)

	def draw(self, window: pygame.Surface, pos):
		# Draw image centered on the center of the base image
		window.blit(self.image, self.image.get_rect(center=self.get_rect(pos).center))