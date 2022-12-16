import pygame

from data.modules.image import Image


class Player:
	def __init__(self, pos):
		# Creates a position object that is a pygame.Vector2
		# A Vector2 has 2 points (x, y), and is useful to store things like position
		# If you are familiar with vectors in physics or math, it can be used to those purposes too
		self.pos = pygame.Vector2(pos)

		# Input is also a vector, for conveniences in adding or multiplying with other values
		self.input = pygame.Vector2()

		# Make an image
		self.image = Image("player", 5, 45)

		# Rect from our image
		self.rect = self.image.get_rect(self.pos)

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

		# If player goes off the edge of the screen, loop back around
		if self.rect.right < 0:
			# Sets the left of the player to the right of the screen, so we are just barely off-screen
			self.rect.left = 800

			# We need to re-update our position, so we set it to the center of the newly updated rect
			# We need to repeat this for every following if statement, because rect stores values as integers, while our position is in floats
			# If we do this outside of the if statement, we would lose precision every frame (Going from decimals to no decimals).
			self.pos = self.rect.center
		elif self.rect.left > 800:
			self.rect.right = 0
			self.pos = self.rect.center
		if self.rect.bottom < 0:
			self.rect.top = 800
			self.pos = self.rect.center
		elif self.rect.top > 800:
			self.rect.bottom = 0
			self.pos = self.rect.center

	# `window: pygame.Surface` is called type hinting. It allows your IDE (pycharm in this case) to give you better autocompletion and error checking
	def draw(self, window: pygame.Surface):
		self.image.draw(window, self.pos)
