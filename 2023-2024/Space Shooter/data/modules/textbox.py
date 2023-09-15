import os

import pygame
import pygame.freetype

from data.modules.files import ASSET_DIR


class TextBox:
	def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
		self.pos = pygame.Vector2(pos)
		self.size = size

		self.rect = pygame.Rect(pos, size)
		self.rect.center = self.pos

		self.selected = False

		self.write_time_wait = 2
		self.last_write_time = 0

		self.text = ""

		self.base_colour = (20, 20, 20)
		self.hover_colour = (50, 50, 50)
		self.selected_colour = (100, 100, 100)

		self.colour = self.base_colour

		self.font = pygame.font.Font(os.path.join(ASSET_DIR, "moonrising.ttf"), int(size[1] * 0.75))

	def write(self, event):
		if self.selected:
			if pygame.time.get_ticks() - self.last_write_time >= self.write_time_wait:
				if event.key == pygame.K_RETURN:
					return True

				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]

				elif event.key == pygame.K_ESCAPE:
					self.selected = False

				else:
					if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
						self.text += event.unicode.upper()
					else:
						self.text += event.unicode.lower()

	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_state = pygame.mouse.get_pressed()

		# Selection
		if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			self.colour = self.hover_colour

			if mouse_state[0]:
				self.selected = True
		else:
			self.colour = self.base_colour

			if mouse_state[0]:
				self.selected = False

		if self.selected:
			self.colour = self.selected_colour

		return self.selected

	def draw(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.colour, self.rect)

		text_image = self.font.render(self.text, True, (255, 255, 255))
		text_rect: pygame.Rect = text_image.get_rect()

		text_surf = pygame.Surface((self.rect.width - 10, self.rect.height), flags=pygame.SRCALPHA)
		text_surf.blit(text_image, (0, 0))
		text_surf.convert_alpha()

		surface.blit(text_surf, (self.rect.left + 5, self.rect.top))

		if self.selected:
			pygame.draw.rect(surface, "white", pygame.Rect(self.rect.left + text_rect.width + 10, self.rect.top + self.rect.height * 0.05, 5, self.rect.height * 0.8))
