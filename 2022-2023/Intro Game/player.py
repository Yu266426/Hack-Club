import pygame


class Player:
	def __init__(self, image: pygame.Surface, pos):
		self.speed = 700.0

		self.image = image
		self.pos = pygame.Vector2(pos)
		self.rect = self.image.get_rect(midtop=self.pos)

		self.x_input = 0

	def update(self, delta: float):
		keys_pressed = pygame.key.get_pressed()

		self.x_input = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]

		self.pos.x += self.x_input * self.speed * delta

		self.rect.midtop = self.pos

		if self.rect.left > 600:
			self.rect.right = 0
			self.pos.update(self.rect.midtop)
		if self.rect.right < 0:
			self.rect.left = 600
			self.pos.update(self.rect.midtop)

	def draw(self, screen: pygame.Surface):
		screen.blit(self.image, self.rect)
