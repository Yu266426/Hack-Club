from typing import Type

import pygame

from data.modules.components.position import Position
from data.modules.game.group import Group
from data.modules.projectiles.projectile import Projectile


class Shooter:
	def __init__(self, pos: Position, projectile: Type[Projectile], projectile_container: Group, cooldown_amount: int | float, position_offset: tuple[int, int] = (0, 0)):
		self.pos: Position = pos

		self.projectile = projectile
		self.projectile_container: Group = projectile_container

		self.offset: pygame.Vector2 = pygame.Vector2(position_offset)

		self.is_shooting: bool = False

		self.cooldown_timer = 0
		self.cooldown_amount = cooldown_amount

	def handle_events(self, mouse_input):
		if mouse_input[0]:
			self.is_shooting = True
		else:
			self.is_shooting = False

	def update(self, delta):
		# If shooting and if it is possible to shoot, fire
		if self.is_shooting and self.cooldown_timer <= 0:
			self.projectile_container.add(self.projectile(self.pos.center + self.offset.rotate(-self.pos.angle), self.pos))

			self.cooldown_timer = self.cooldown_amount

		# Counts down
		if self.cooldown_timer > 0:
			self.cooldown_timer -= delta

			if self.cooldown_timer < 0:
				self.cooldown_timer = 0
