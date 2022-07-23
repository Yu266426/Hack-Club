import pygame


# Player class
class Player:
	def __init__(self, pos, size):
		# Basic info
		self.x_movement = 0
		self.speed = 7

		# Creates a surface at the size we specified
		self.image = pygame.Surface(size)
		# Makes our image red
		self.image.fill("red")
		# Gets a rectangle from the surface, and sets the center to the position we specified
		self.rect = self.image.get_rect(center=pos)

		# Gets the display we are drawing onto
		self.display = pygame.display.get_surface()

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

		# Wraps our player around to the other side of the screen
		# If we are to the left of the screen
		if self.rect.right < 0:
			self.rect.left = self.display.get_width()
		elif self.rect.left > self.display.get_width():
			self.rect.right = 0

	def draw(self):
		# Draws, or "blits" our image to the display at wherever our rect is
		self.display.blit(self.image, self.rect)
