import pygame


class Player:
	def __init__(self, ball_pos):
		self.angle = 0

		self.ball_pos = pygame.Vector2(ball_pos)

		offset = pygame.Vector2(0, -80).rotate(self.angle)
		self.pos = self.ball_pos + offset

		self.image = pygame.transform.scale_by(pygame.image.load("player.png"), 0.6)
		self.rect = self.image.get_rect(center=self.pos)

	def update(self):
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_d]:
			self.angle += 3
		if keys_pressed[pygame.K_a]:
			self.angle -= 3

		self.angle = min(60, max(-60, self.angle))

		offset = pygame.Vector2(0, -80).rotate(self.angle)
		self.pos = self.ball_pos + offset

		self.rect.center = self.pos

	def draw(self, surface: pygame.Surface):
		# pygame.draw.circle(surface, "white", self.pos, 20)

		image = pygame.transform.rotate(self.image, 180 - self.angle)
		surface.blit(image, image.get_rect(center=self.rect.center))
