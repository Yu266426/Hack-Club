import pygame

from data.modules.components.position import Position


class Controller:
	def __init__(self, pos: Position, acceleration_speed: float, drag: float):
		self.pos = pos

		self.input = pygame.Vector2()

		self.acceleration_speed: float = acceleration_speed
		self.drag: float = drag

		self.velocity: pygame.Vector2 = pygame.Vector2()
		self.acceleration: pygame.Vector2 = pygame.Vector2()

	def handle_input(self, keys_pressed):
		self.input.x = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
		self.input.y = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]

	def update(self, delta: float):
		# Calculate forces (And makes it so diagonal movement doesn't make the player faster)
		if self.input.length() != 0:
			self.acceleration = self.input.normalize() * self.acceleration_speed
		else:
			self.acceleration.xy = 0, 0

		self.acceleration -= self.drag * self.velocity

		self.velocity += self.acceleration * delta

		# Update position
		self.pos.pos += self.velocity * delta
