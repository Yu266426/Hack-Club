import pygame

from data.modules.components.damage import Damage
from data.modules.components.health import Health
from data.modules.components.position import Position
from data.modules.components.rotatable_image import RotatableImage
from data.modules.game.contants import ASTEROID_ATTRIBUTES
from data.modules.game.game_object import GameObject
from data.modules.game.helper import get_angled_offset, get_random_float
from data.modules.game.image_loader import ImageLoader


class Asteroid(GameObject):
	def __init__(self, pos: tuple[int, int], direction: float, asteroid_name: str, spawner_pos: Position):
		super().__init__(pos, ASTEROID_ATTRIBUTES[asteroid_name]["radius"], angle=get_random_float(0, 360))

		self.image = RotatableImage(self.pos, ImageLoader.get_image(asteroid_name))
		self.pos.generate_center(self.image.center_offset)

		self.direction = direction

		self.movement = get_angled_offset(self.direction, get_random_float(ASTEROID_ATTRIBUTES[asteroid_name]["speed"][0], ASTEROID_ATTRIBUTES[asteroid_name]["speed"][1]))
		self.rotation_speed = get_random_float(-ASTEROID_ATTRIBUTES[asteroid_name]["rotation"], ASTEROID_ATTRIBUTES[asteroid_name]["rotation"])

		self.health = Health(ASTEROID_ATTRIBUTES[asteroid_name]["health"])
		self.damage = Damage(ASTEROID_ATTRIBUTES[asteroid_name]["damage"])

		self.spawner_pos = spawner_pos
		self.despawn_distance = 1000

	def update(self, delta: float, scroll: pygame.Vector2):
		self.pos.move_with_vector(self.movement * delta)

		self.pos.angle += self.rotation_speed * delta
		self.image.update_angle()

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		self.image.draw(display, scroll)

	def check_death(self):
		return not self.health.check_alive() or self.pos.pos.distance_to(self.spawner_pos.pos) > self.despawn_distance
