import pygame

from data.modules.components.damage import Damage
from data.modules.components.position import Position
from data.modules.game.game_object import GameObject


class Projectile(GameObject):
	def __init__(self, spawn_pos: tuple[int, int] | pygame.Vector2, spawner_pos: Position, radius: float, damage: int):
		super().__init__(spawn_pos, radius, angle=spawner_pos.angle)
		self.spawner_pos = spawner_pos

		self.starting_pos = spawner_pos.pos.copy()

		self.damage = Damage(damage)
