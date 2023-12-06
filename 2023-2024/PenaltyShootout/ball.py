import pygame


class Ball:
	def __init__(self, pos, velocity):
		# self.pos = pygame.Vector2(pos)

		self.velocity = pygame.Vector2(velocity)

		self.image = pygame.image.load("soccer_ball.png")
		self.image = pygame.transform.scale(self.image, (40, 40))

		self.rect = self.image.get_frect(center=pos)
		self.prev_rect = self.rect.copy()

	def shoot_ball(self, angle: float, speed: float):
		direction_vector = pygame.Vector2(0, -speed).rotate(angle)

		self.velocity += direction_vector

	def update(self, obstacles):
		self.velocity -= self.velocity * 0.01
		self.prev_rect = self.rect.copy()

		# X movement
		# self.pos.x += self.velocity.x
		# self.rect.center = self.pos
		self.rect.x += self.velocity.x

		for obstacle in obstacles:
			if self.rect.colliderect(obstacle):
				self.velocity.x *= -1

				if obstacle.rect.left <= self.rect.right and self.prev_rect.right <= obstacle.prev_rect.left:
					self.rect.right = obstacle.rect.left
				# self.pos.x = self.rect.centerx

				if self.rect.left <= obstacle.rect.right and obstacle.prev_rect.right <= self.prev_rect.left:
					self.rect.left = obstacle.rect.right
		# self.pos.x = self.rect.centerx

		if self.rect.left < 0:
			self.velocity.x *= -1
		if self.rect.right > 600:
			self.velocity.x *= -1

		# Y movement
		# self.pos.y += self.velocity.y
		# self.rect.center = self.pos
		self.rect.y += self.velocity.y

		for obstacle in obstacles:
			if self.rect.colliderect(obstacle):
				self.velocity.y *= -1

				if obstacle.rect.top <= self.rect.bottom and self.prev_rect.bottom <= obstacle.prev_rect.top:
					self.rect.bottom = obstacle.rect.top
				# self.pos.y = self.rect.centery
				if self.rect.top <= obstacle.rect.bottom and obstacle.prev_rect.bottom <= self.prev_rect.top:
					self.rect.top = obstacle.rect.bottom
		# self.pos.y = self.rect.centery

		if self.rect.top < 0:
			self.velocity.y *= -1
		if self.rect.bottom > 600:
			self.velocity.y *= -1

	def draw(self, surface: pygame.Surface):
		surface.blit(self.image, self.rect)
