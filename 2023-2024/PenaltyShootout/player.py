import pygame


class Player:
	def __init__(self, ball_pos):
		self.angle = 0

		self.ball_pos = pygame.Vector2(ball_pos)

		offset = pygame.Vector2(0, -80).rotate(self.angle)
		self.pos = self.ball_pos + offset

	def update(self):
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_d]:
			self.angle += 3
		if keys_pressed[pygame.K_a]:
			self.angle -= 3

		self.angle = min(60, max(-60, self.angle))

		offset = pygame.Vector2(0, -80).rotate(self.angle)
		self.pos = self.ball_pos + offset

	def draw(self, surface):
		pygame.draw.circle(surface, "white", self.pos, 20)
