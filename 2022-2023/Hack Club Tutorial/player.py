import pygame


class Player:
	# Self indicates that every player we make will have a unique copy of everything we've listed
	def __init__(self, pos):
		self.speed = 10

		self.image = pygame.Surface((40, 80))
		self.image.fill("red")
		self.rect = self.image.get_rect(center=pos)

	def update(self):
		keys = pygame.key.get_pressed()  # All keys down on this frame

		x_input = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]  # 1 for right, -1 for left, 0 for not moving

		self.rect.x += x_input * self.speed  # Moves our rectangle

		if self.rect.left > 500:  # Keeps our player in the screen
			self.rect.right = 0
		if self.rect.right < 0:
			self.rect.left = 500

	def draw(self, surface):  # Our window is a pygame.Surface
		surface.blit(self.image, self.rect)  # Blit just means to draw to the screen
