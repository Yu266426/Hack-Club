import pygame

from images import PLAYER_IMAGE


class Player:
	def __init__(self):
		self.pos = pygame.Vector2((400, 400))

		self.image = PLAYER_IMAGE.convert_alpha()
		self.image = pygame.transform.scale(self.image, (50, 50))

		self.rect = self.image.get_rect(center=self.pos)

		self.input = pygame.Vector2()

		self.speed = 5
		self.drag = 0.3

		self.acceleration = pygame.Vector2()
		self.velocity = pygame.Vector2()

	def update(self):
		keys = pygame.key.get_pressed()
		self.input.x = keys[pygame.K_d] - keys[pygame.K_a]
		self.input.y = keys[pygame.K_s] - keys[pygame.K_w]

		if self.input.length() != 0:
			self.input.normalize_ip()

		self.acceleration = self.input * self.speed

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
