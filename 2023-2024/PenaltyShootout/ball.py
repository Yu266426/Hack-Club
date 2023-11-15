import pygame


class Ball:
	def __init__(self, pos, velocity):
		self.pos = pygame.Vector2(pos)

		self.velocity = pygame.Vector2(velocity)

		self.image = pygame.image.load("soccer_ball.png")
		self.image = pygame.transform.scale(self.image, (40, 40))

		self.rect = self.image.get_rect(center=self.pos)

	def shoot_ball(self, angle: float, speed: float):
		direction_vector = pygame.Vector2(0, -speed).rotate(angle)

		self.velocity += direction_vector

	def update(self):
		self.velocity -= self.velocity * 0.01

		self.pos.x += self.velocity.x
		self.rect.center = self.pos

		if self.rect.left < 0:
			self.velocity.x *= -1
		if self.rect.right > 600:
			self.velocity.x *= -1

		self.pos.y += self.velocity.y
		self.rect.center = self.pos

		if self.rect.top < 0:
			self.velocity.y *= -1
		if self.rect.bottom > 600:
			self.velocity.y *= -1

	def draw(self, surface: pygame.Surface):
		surface.blit(self.image, self.rect)
