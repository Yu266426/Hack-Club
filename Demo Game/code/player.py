import pygame


class Player:
	def __init__(self, pos, size):
		self.x_movement = 0
		self.speed = 7

		self.pos = pygame.Vector2(pos)

		self.image = pygame.Surface(size)
		self.image.fill("red")

		self.rect = self.image.get_rect(center=self.pos)

		self.display = pygame.display.get_surface()

	def get_input(self):
		keys_pressed = pygame.key.get_pressed()

		self.x_movement = (keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]) + (keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT])

	def update(self, delta):
		self.get_input()

		self.pos.x += self.x_movement * self.speed * delta
		self.rect.center = self.pos

		if self.rect.right < 0:
			self.rect.left = self.display.get_width()
			self.pos.x = self.rect.centerx
		elif self.rect.left > self.display.get_width():
			self.rect.right = 0
			self.pos.x = self.rect.centerx

	def draw(self):
		self.display.blit(self.image, self.rect)
