import pygame


class Box:
	def __init__(self):
		self.speed = 15

		self.image = pygame.Surface((40, 80))
		self.image.fill("black")

		self.rect = self.image.get_rect(midbottom=(250, 0))

	def update(self):
		self.rect.y += self.speed

	def draw(self, surface):
		surface.blit(self.image, self.rect)
