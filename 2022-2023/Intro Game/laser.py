import pygame


class Laser:
	def __init__(self, image: pygame.Surface, pos):
		self.speed = 1000.0

		self.image = image
		self.pos = pygame.Vector2(pos)
		self.rect = self.image.get_rect(midtop=self.pos)

	def update(self, delta: float):
		self.pos.y -= self.speed * delta
		self.rect.midtop = self.pos

	def draw(self, screen: pygame.Surface):
		screen.blit(self.image, self.rect)
