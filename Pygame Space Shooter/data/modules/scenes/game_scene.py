import pygame

from data.modules.asteroids.asteroid import Asteroid
from data.modules.asteroids.asteroid_spawner import AsteroidSpawner
from data.modules.effects.particle import spawn_particles
from data.modules.effects.star import generate_stars
from data.modules.game.collisions import group_circle_collisions, single_group_circle_collisions
from data.modules.game.contants import WINDOW_SIZE, FOLLOW_ROOM
from data.modules.game.events import PLAYER_DEATH_EVENT
from data.modules.game.group import Group
from data.modules.game.helper import get_random_float
from data.modules.player.player import Player
from data.modules.scenes.base_scene import BaseScene


class GameScene(BaseScene):
	def __init__(self):
		super().__init__()

		self.scroll = pygame.Vector2()

		self.stars = Group()
		generate_stars(self.stars, 80)

		self.projectiles = Group()

		self.particles = Group()

		self.player = Player(self.projectiles)

		self.asteroids = Group()

		self.asteroid_spawner = AsteroidSpawner(self.asteroids, self.player)

	def handle_events(self, keys_pressed, mouse_pressed, mouse_pos, key_downs, key_ups):
		# Handle inputs
		self.player.handle_events(keys_pressed, mouse_pressed, mouse_pos, self.scroll)

	def update_scroll(self, target_pos: pygame.Vector2 | tuple[int, int], delta: float):
		target_x = target_pos[0] - WINDOW_SIZE[0] / 2
		target_y = target_pos[1] - WINDOW_SIZE[1] / 2

		self.scroll += pygame.Vector2((target_x - self.scroll.x) / FOLLOW_ROOM, (target_y - self.scroll.y) / FOLLOW_ROOM) * delta

	def handle_projectile_asteroid_collisions(self):
		collided_list = group_circle_collisions(self.projectiles, self.asteroids)

		for projectile in collided_list:
			for asteroid in collided_list[projectile]:
				spawn_particles(self.particles, projectile.pos.pos, 3, (6, 15), "laser", direction=projectile.pos.angle)

				self.projectiles.remove(projectile)

				asteroid.health.damage(projectile.damage)

				if asteroid.check_death():
					spawn_particles(self.particles, asteroid.pos.center, asteroid.pos.radius, (80, 120), "large asteroid", direction=asteroid.direction)
					self.asteroids.remove(asteroid)

	def handle_player_asteroid_collisions(self):
		collided_list = single_group_circle_collisions(self.player, self.asteroids)

		for asteroid in collided_list:
			asteroid: Asteroid

			self.player.health.damage(asteroid.damage)

			if self.player.check_death():
				# TODO: finish player death explosion, and wait before quiting
				spawn_particles(self.particles, asteroid.pos.center, asteroid.pos.radius, (80, 120), "large asteroid", direction=asteroid.direction)

				pygame.event.post(PLAYER_DEATH_EVENT)
			else:
				asteroid.health.damage(self.player.damage)

				if asteroid.check_death():
					spawn_particles(self.particles, asteroid.pos.center, asteroid.pos.radius, (80, 120), "large asteroid")
					self.asteroids.remove(asteroid)

	def update(self, delta: float):
		self.update_scroll(self.player.pos.center, delta)

		# Update objects
		self.stars.update(delta, self.scroll)

		self.player.update(delta, self.scroll)

		self.projectiles.update(delta, self.scroll)
		self.projectiles.check_death()

		self.asteroids.update(delta, self.scroll)
		self.asteroids.check_death()

		self.handle_projectile_asteroid_collisions()
		self.handle_player_asteroid_collisions()

		self.particles.update(delta, self.scroll)
		self.particles.check_death()

		self.asteroid_spawner.update(delta)

	def draw(self, window: pygame.Surface):
		window.fill((0, 0, 0))

		self.stars.draw(window, self.scroll)

		self.projectiles.draw(window, self.scroll)

		self.asteroids.draw(window, self.scroll)

		self.player.draw(window, self.scroll)

		self.particles.draw(window, self.scroll)
