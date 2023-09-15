import pygame


class Particle:
	def __init__(self, pos, initial_velocity, colour, size):
		self.pos = pygame.Vector2(pos)
		self.velocity = pygame.Vector2(initial_velocity)

		self.colour = colour
		self.size = size

	def update(self, delta: float):
		self.pos += self.velocity * delta

		self.velocity -= self.velocity * 0.99 * delta
		self.size -= self.size * 0.9 * delta

	def draw(self, screen: pygame.Surface):
		pygame.draw.rect(screen, self.colour, (*self.pos, self.size, self.size))
