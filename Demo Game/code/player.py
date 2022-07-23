import pygame


# Player class
class Player:
	def __init__(self, pos, size):
		self.x_movement = 0
		self.speed = 5

		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect(center=pos)

	def get_input(self):
		# Gets all the keys pressed on this frame
		keys_pressed = pygame.key.get_pressed()

		# Checks to see left or right movement, with a little logic to shorten things
		self.x_movement = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]

	def update(self):
		# Gets our input
		self.get_input()

		# Moves our rect
		self.rect.x += self.x_movement * self.speed

	def draw(self, display):
		# Draws, or "blits" our image to the display at wherever our rect is
		display.blit(self.image, self.rect)
