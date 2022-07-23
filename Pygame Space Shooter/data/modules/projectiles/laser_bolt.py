import pygame

from data.modules.components.position import Position
from data.modules.components.rotatable_image import RotatableImage
from data.modules.game.helper import get_angled_offset
from data.modules.game.image_loader import ImageLoader
from data.modules.projectiles.projectile import Projectile


class LaserBolt(Projectile):
	def __init__(self, spawn_pos: tuple[int, int] | pygame.Vector2, spawner_pos: Position):
		super().__init__(spawn_pos, spawner_pos, 10, 5)

		self.image = RotatableImage(self.pos, ImageLoader.images["laser"])
		self.pos.generate_center(self.image.center_offset)
		self.pos.center_self()

		self.movement = get_angled_offset(self.pos.angle, 35)

		self.despawn_distance = 700

	def update(self, delta: float, scroll: pygame.Vector2):
		self.pos.pos += self.movement * delta

	def check_death(self):
		if self.pos.pos.distance_to(self.starting_pos) > self.despawn_distance or self.pos.pos.distance_to(self.spawner_pos.pos) > self.despawn_distance:
			return True
		else:
			return False

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		self.image.draw(display, scroll)
