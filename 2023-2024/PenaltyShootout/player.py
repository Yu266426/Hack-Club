import pygame


class Player:
	def __init__(self):
		self.pos = pygame.Vector2((300, 300))

	def move(self):
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_d]:
			self.pos.x += 5
		if keys_pressed[pygame.K_a]:
			self.pos.x -= 5

		if self.pos.x - 20 < 0:
			self.pos.x = 20
		if self.pos.x + 20 > 600:
			self.pos.x = 600 - 20

	def draw(self, surface):
		pygame.draw.circle(surface, "white", self.pos, 20)
