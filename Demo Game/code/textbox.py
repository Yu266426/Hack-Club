import pygame
import pygame.freetype


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

		self.font = pygame.freetype.SysFont("arial", int(size[1] * 0.75))

	def write(self, event: pygame.event.Event, time: int):
		if self.selected:
			if time - self.last_write_time >= self.write_time_wait:
				if event.key == pygame.K_RETURN:
					return True

				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]

				else:
					if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
						self.text += event.unicode.upper()
					else:
						self.text += event.unicode.lower()

	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_state = pygame.mouse.get_pressed()

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

		rendered_text = self.font.render(self.text, (255, 255, 255))
		text_image: pygame.Surface = rendered_text[0].convert_alpha()

		text_surf = pygame.Surface((self.rect.width - 10, self.rect.height), flags=pygame.SRCALPHA)
		text_surf.blit(text_image, (0, 0))
		text_surf.convert_alpha()

		surface.blit(text_surf, (self.rect.left + 5, self.rect.top + 7))
