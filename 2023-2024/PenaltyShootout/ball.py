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

	def update(self, obstacles):
		self.velocity -= self.velocity * 0.01

		# X movement
		self.pos.x += self.velocity.x
		self.rect.center = self.pos

		for obstacle in obstacles:
			if self.rect.colliderect(obstacle):
				self.pos.x -= self.velocity.x
				self.velocity.x *= -1

		if self.rect.left < 0:
			self.velocity.x *= -1
		if self.rect.right > 600:
			self.velocity.x *= -1

		# Y movement
		self.pos.y += self.velocity.y
		self.rect.center = self.pos

		for obstacle in obstacles:
			if self.rect.colliderect(obstacle):
				self.pos.y -= self.velocity.y
				self.velocity.y *= -1

		if self.rect.top < 0:
			self.velocity.y *= -1
		if self.rect.bottom > 600:
			self.velocity.y *= -1

	def draw(self, surface: pygame.Surface):
		surface.blit(self.image, self.rect)
