import pygame


class Player:
	def __init__(self):
		self.pos = pygame.Vector2((400, 400))

		self.image = pygame.Surface((40, 40))
		self.image.fill("red")
		self.rect = self.image.get_rect(center=self.pos)

		self.speed = 10
		self.drag = 0.5

		self.acceleration = pygame.Vector2()
		self.velocity = pygame.Vector2()

	def update(self):
		keys = pygame.key.get_pressed()
		x_input = keys[pygame.K_d] - keys[pygame.K_a]
		y_input = keys[pygame.K_s] - keys[pygame.K_w]

		self.acceleration.x = x_input * self.speed
		self.acceleration.y = y_input * self.speed

		self.velocity += self.acceleration
		self.velocity -= self.velocity * self.drag

		self.pos += self.velocity

		self.rect.center = self.pos

		if self.rect.left > 800:
			self.rect.right = 0
			self.pos.update(self.rect.center)

		elif self.rect.right < 0:
			self.rect.left = 800
			self.pos.update(self.rect.center)

		if self.rect.top > 800:
			self.rect.bottom = 0
			self.pos.update(self.rect.center)
		elif self.rect.bottom < 0:
			self.rect.top = 800
			self.pos.update(self.rect.center)

	def draw(self, screen):
		screen.blit(self.image, self.rect)
