import pygame


class Player:
	def __init__(self):
		self.pos = [400, 200]

		self.image = pygame.Surface((60, 60))
		self.image.fill("red")

	def draw(self, screen):
		screen.blit(self.image, self.pos)
