import random

import pygame

from data.modules.asteroids.asteroid import Asteroid
from data.modules.game.group import Group
from data.modules.game.helper import get_angled_offset, get_random_float, get_angle_to
from data.modules.player.player import Player


class AsteroidSpawner:
	def __init__(self, asteroid_group: Group, player: Player):
		self.asteroid_group = asteroid_group
		self.player = player

		self.spawn_cooldown = 120.0
		self.spawn_rate = 200.0

	def spawn_asteroids(self):
		for loop in range(random.randint(1, 3)):
			# Offset from player
			if self.player.controller.input.length() == 0:
				# Player isn't moving, so comes from all angles
				offset = get_angled_offset(get_random_float(0, 360), 800)
			else:
				# Player moving, place in front so that they run into the asteroids
				direction = -pygame.Vector2(0, 0).angle_to(self.player.controller.input) + get_random_float(-50, 50)
				offset = get_angled_offset(direction, 800)

			spawn_position = self.player.controller.pos.pos + offset
			angle = get_angle_to(spawn_position, self.player.controller.pos.pos) + get_random_float(-10, 10)

			self.asteroid_group.add(Asteroid(spawn_position, angle, "large asteroid", self.player.pos))

	def update(self, delta: float):
		if self.spawn_cooldown < 0:
			self.spawn_asteroids()

			# Add cooldown
			self.spawn_cooldown = float(self.spawn_rate)

			# Increase spawn rate (reduce time between spawns)
			self.spawn_rate /= 1.05
			if self.spawn_rate < 30:
				self.spawn_rate = 30
		else:
			if self.spawn_cooldown > 0:
				self.spawn_cooldown -= delta
			else:
				self.spawn_cooldown = 0
