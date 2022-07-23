import pygame

from data.modules.components.controller import Controller
from data.modules.components.damage import Damage
from data.modules.components.health import Health
from data.modules.components.rotatable_image import RotatableImage
from data.modules.components.shooter import Shooter
from data.modules.game.game_object import GameObject
from data.modules.game.group import Group
from data.modules.game.helper import get_angle_to
from data.modules.game.image_loader import ImageLoader
from data.modules.projectiles.laser_bolt import LaserBolt


class Player(GameObject):
	def __init__(self, projectiles_group: Group):
		super().__init__((400, 400), 20)

		self.image = RotatableImage(self.pos, ImageLoader.images["player"])
		self.pos.generate_center(self.image.center_offset)
		self.pos.center_self()

		self.controller = Controller(self.pos, 2.3, 0.14)

		self.shooter = Shooter(self.pos, LaserBolt, projectiles_group, 10, (15, 0))

		self.health = Health(100)
		self.damage = Damage(100)

	def handle_events(self, keys_pressed, mouse_pressed, mouse_pos: tuple[int, int], scroll: pygame.Vector2):
		self.pos.angle = get_angle_to(self.pos.center - scroll, mouse_pos)

		self.image.update_angle()
		self.controller.handle_input(keys_pressed)

		self.shooter.handle_events(mouse_pressed)

	def update(self, delta: float, scroll: pygame.Vector2):
		self.controller.update(delta)

		self.shooter.update(delta)

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		self.image.draw(display, scroll)

	def check_death(self):
		return not self.health.check_alive()
