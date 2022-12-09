import pygame


class Player:
	def __init__(self, pos):
		self.pos = pygame.Vector2(pos)
		self.input = pygame.Vector2()

		self.image = pygame.Surface((60, 60))
		self.image.fill("red")

		self.rect = self.image.get_rect(center=self.pos)

	def update(self):
		keys_pressed = pygame.key.get_pressed()
		self.input.x = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
		self.input.y = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]

		self.rect.center += self.input * 5

	def draw(self, window: pygame.Surface):
		window.blit(self.image, self.rect)
