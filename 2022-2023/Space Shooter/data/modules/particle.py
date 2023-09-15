import random

import pygame

from data.modules.constants import ParticleTypes
from data.modules.utils import get_angled_offset

particle_info = {
	ParticleTypes.Laser: {"size": (8, 12), "speed": (3, 7), "decay": (2, 6), "colour": ((252, 207, 3), (255, 248, 43), (255, 166, 0))},
	ParticleTypes.LargeAsteroid: {"size": (14, 22), "speed": (3, 5), "decay": (3, 5), "colour": ((235, 143, 30), (235, 62, 14), (255, 208, 54))},
	ParticleTypes.MediumAsteroid: {"size": (9, 17), "speed": (4, 6), "decay": (4, 6), "colour": ((240, 109, 23), (246, 143, 35), (245, 162, 25))},
	ParticleTypes.PlayerExplosionBlast: {"size": (20, 34), "speed": (1, 4), "decay": (3, 7), "colour": ((235, 143, 30), (235, 62, 14), (255, 208, 54), (240, 109, 23), (246, 143, 35), (245, 162, 25), (252, 207, 3), (255, 248, 43), (255, 166, 0))},
	ParticleTypes.PlayerExplosionArm: {"size": (13, 20), "speed": (3, 7), "decay": (1, 3), "colour": ((235, 143, 30), (235, 62, 14), (255, 208, 54), (240, 109, 23), (246, 143, 35), (245, 162, 25), (252, 207, 3), (255, 248, 43), (255, 166, 0))},
	ParticleTypes.PlayerTrail: {"size": (5, 8), "speed": (1, 2), "decay": (2, 5), "colour": ((3, 232, 252), (32, 179, 247), (0, 226, 230))}
}


class Particle:
	def __init__(self, particle_type, pos, direction=None):
		self.pos = pygame.Vector2(pos)

		speed = random.randint(particle_info[particle_type]["speed"][0], particle_info[particle_type]["speed"][1])
		if direction is None:
			self.movement = get_angled_offset(random.randint(0, 360), speed)
		else:
			self.movement = direction.normalize().rotate(random.randint(-20, 20)) * speed

		self.size = random.randint(particle_info[particle_type]["size"][0], particle_info[particle_type]["size"][1])
		self.decay = random.randint(particle_info[particle_type]["decay"][0], particle_info[particle_type]["decay"][1]) / 5.0
		self.colour = random.choice(particle_info[particle_type]["colour"])

	def check_size(self):
		return self.size <= 0.1

	def update(self, delta):
		self.pos += self.movement * delta

		self.size -= self.decay * delta

	def draw(self, surface, scroll):
		pygame.draw.rect(surface, self.colour, (self.pos - scroll - pygame.Vector2(self.size / 2, self.size / 2), (self.size, self.size)))
