import pygame


class Goal:
	def __init__(self, pos):
		self.pos = pygame.Vector2(pos)

		self.image = pygame.image.load("soccer_goal.png")
		self.image = pygame.transform.scale_by(self.image, 0.6)
		self.rect = self.image.get_rect(center=self.pos)

	def draw(self, surface: pygame.Surface):
		surface.blit(self.image, self.rect)
