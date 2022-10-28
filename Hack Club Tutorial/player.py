import pygame


class Player:
	def __init__(self, pos):
		self.speed = 10

		self.image = pygame.Surface((40, 80))
		self.image.fill("red")
		self.rect = self.image.get_rect(center=pos)

	def update(self):
		keys = pygame.key.get_pressed()

		x_input = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

		self.rect.x += x_input * self.speed

		if self.rect.left > 500:
			self.rect.right = 0
		if self.rect.right < 0:
			self.rect.left = 500

	def draw(self, surface):
		surface.blit(self.image, self.rect)
