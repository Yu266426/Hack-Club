import pygame


# Player class
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
		# Gets all the keys pressed on this frame
		keys_pressed = pygame.key.get_pressed()

		# Checks to see left or right movement, with a little logic to shorten things
		self.x_movement = (keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]) + (keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT])

	def update(self, delta):
		# Gets our input
		self.get_input()

		# Moves our rect
		self.pos.x += self.x_movement * self.speed * delta
		self.rect.center = self.pos

		# Wraps our player around to the other side of the screen
		# If we are to the left of the screen
		if self.rect.right < 0:
			self.rect.left = self.display.get_width()
			self.pos.x = self.rect.centerx
		elif self.rect.left > self.display.get_width():
			self.rect.right = 0
			self.pos.x = self.rect.centerx

	def draw(self):
		# Draws, or "blits" our image to the display at wherever our rect is
		self.display.blit(self.image, self.rect)
