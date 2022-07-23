import random

import pygame

from data.modules.components.image import Image
from data.modules.game.contants import PARTICLE_ATTRIBUTES
from data.modules.game.game_object import GameObject
from data.modules.game.group import Group
from data.modules.game.helper import get_angled_offset, get_random_float


def spawn_particles(particle_list: Group, pos: pygame.Vector2, radius: float, amount: tuple[int, int], type: str, direction: float | None = None):
	for _ in range(random.randint(amount[0], amount[1])):
		spawn_pos = pos + get_angled_offset(get_random_float(0, 360), get_random_float(0, radius))

		spawn_direction = direction
		if spawn_direction is not None:
			spawn_direction += get_random_float(-30, 30)

		particle_list.add(Particle(spawn_pos, type, spawn_direction))


class Particle(GameObject):
	def __init__(self, pos: tuple[int, int] | pygame.Vector2, type: str, direction: float | None = None):
		if direction is None:
			direction = get_random_float(0, 360)

		super().__init__(pos, get_random_float(PARTICLE_ATTRIBUTES[type]["size"][0], PARTICLE_ATTRIBUTES[type]["size"][1]), angle=direction)

		self.image = Image(self.pos, pygame.Surface((self.pos.radius / 2, self.pos.radius / 2)), colour=random.choice(PARTICLE_ATTRIBUTES[type]["colour"]))

		self.movement = get_angled_offset(direction, get_random_float(PARTICLE_ATTRIBUTES[type]["speed"][0], PARTICLE_ATTRIBUTES[type]["speed"][1]))

		self.decay = get_random_float(PARTICLE_ATTRIBUTES[type]["decay"][0], PARTICLE_ATTRIBUTES[type]["decay"][1])

	def update(self, delta: float, scroll: pygame.Vector2):
		self.pos.radius -= self.decay * delta
		self.image.scale_image((self.pos.radius / 2, self.pos.radius / 2))

		self.pos.move_with_vector(self.movement * delta)

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		self.image.draw(display, scroll)

	def check_death(self):
		return self.pos.radius <= 7
