import os

import pygame.font

from data.modules.files import ASSET_DIR


class Text:
	def __init__(self, text, pos, font_size, colour):
		self.text = text
		self.pos = pygame.Vector2(pos)

		self.font = pygame.font.Font(os.path.join(ASSET_DIR, "moonrising.ttf"), font_size)
		self.colour = colour

	def draw_left(self, surface):
		rendered_text = self.font.render(self.text, True, self.colour)
		surface.blit(rendered_text, self.pos)

	def draw_centered(self, surface):
		rendered_text = self.font.render(self.text, True, self.colour)
		surface.blit(rendered_text, (self.pos.x - rendered_text.get_width() / 2, self.pos.y))

	def draw_right(self, surface):
		rendered_text = self.font.render(self.text, True, self.colour)
		surface.blit(rendered_text, (self.pos.x - rendered_text.get_width(), self.pos.y))
