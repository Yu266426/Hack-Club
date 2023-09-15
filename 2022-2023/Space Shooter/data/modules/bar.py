import pygame


class Bar:
	def __init__(self, pos, size, background_colour, bar_colour):
		self.pos = pygame.Vector2(pos)

		self.background_rect = pygame.Rect(self.pos, size)
		self.background_colour = background_colour

		self.bar_colour = bar_colour

		self.border = 3

	def draw(self, surface, amount, total):
		pygame.draw.rect(surface, self.background_colour, self.background_rect)

		fill_amount = amount / total
		fill_rect = pygame.Rect(self.pos + pygame.Vector2(self.border, self.border), (fill_amount * (self.background_rect.width - self.border * 2), self.background_rect.height - self.border * 2))
		pygame.draw.rect(surface, self.bar_colour, fill_rect)
