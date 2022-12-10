import pygame


class Player:
	def __init__(self, pos):
		# Creates a position object that is a pygame.Vector2
		# A Vector2 has 2 points (x, y), and is useful to store things like position
		# If you are familiar with vectors in physics or math, it can be used to those purposes too
		self.pos = pygame.Vector2(pos)

		# Input is also a vector, for conveniences in adding or multiplying with other values
		self.input = pygame.Vector2()

		# Make a surface, and fill it with red
		self.image = pygame.Surface((60, 60))
		self.image.fill("red")

		# Rect from our image
		self.rect = self.image.get_rect(center=self.pos)

	def update(self):
		keys_pressed = pygame.key.get_pressed()  # Gets all the keys pressed
		# Sets input to 1 or -1 or 0 depending on what is pressed
		# 1 for right / down, -1 for left / up
		self.input.x = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
		self.input.y = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]

		# Modifies self.pos with the input * speed (5 in this case)
		# Feature of Vector2, where both (x, y) is modified by the multiplication, and can be added to self.pos
		self.pos += self.input * 5

		# Adjusts self.rect.center to be self.pos
		self.rect.center = self.pos

	def draw(self, window: pygame.Surface):
		window.blit(self.image, self.rect)
