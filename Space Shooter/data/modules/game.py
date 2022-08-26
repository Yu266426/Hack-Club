import os.path
import random

import pygame.display

from data.modules.asteroid import Asteroid
from data.modules.bar import Bar
from data.modules.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GameStates, AsteroidTypes, ParticleTypes
from data.modules.files import ASSET_DIR
from data.modules.laser import Laser
from data.modules.particle import Particle
from data.modules.player import Player
from data.modules.star import Star
from data.modules.text import Text
from data.modules.timer import Timer
from data.modules.utils import get_angled_offset, get_angle_to


class Game:
	def __init__(self):
		self.is_running = True
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Space Shooter")
		pygame.display.set_icon(pygame.image.load(os.path.join(ASSET_DIR, "player.png")).convert_alpha())
		self.clock = pygame.time.Clock()

		self.game_state = GameStates.Start

		self.scroll = pygame.Vector2()
		self.screen_shake = 0.0
		self.stars = []
		self.generate_stars(100)

		self.lasers = []
		self.asteroids = []
		self.particles = []

		self.asteroid_spawn_timer = Timer(3, start_on=False)

		self.player = Player((self.scroll.x + SCREEN_WIDTH / 2, self.scroll.y + SCREEN_HEIGHT / 2))
		self.player_shoot_timer = Timer(0.18)
		self.player_trail_timer = Timer(0.02)

		self.death_timer = Timer(6, start_on=False)

		self.score = 0

		self.fire_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "laser fire.wav"))
		self.laser_explosion_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "laser explosion.wav"))
		self.large_asteroid_explosion_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "large asteroid explosion.wav"))
		self.medium_asteroid_explosion_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "medium asteroid explosion.wav"))
		self.player_explosion_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "player explosion.wav"))

		self.start_text = Text("Press Space To Start!", (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2), 60, "white")
		self.health_bar = Bar((10, 10), (300, 50), (50, 50, 50), (50, 200, 50))
		self.score_text = Text("", (SCREEN_WIDTH - 10, 10), 40, "white")
		self.end_score_text = Text("Score: ", (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2), 60, "white")
		self.end_restart_text = Text("Press Space To Restart", (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5), 40, "white")

	def reset(self):
		self.player = Player((self.scroll.x + SCREEN_WIDTH / 2, self.scroll.y - SCREEN_HEIGHT / 2))
		self.score = 0

	def generate_stars(self, n_stars):
		for _ in range(n_stars):
			self.stars.append(Star((random.randint(-10, 810), random.randint(-10, 810)), float(random.randint(35, 70)) / 10))

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.is_running = False

				if self.game_state == GameStates.Start:
					if event.key == pygame.K_SPACE:
						self.game_state = GameStates.Game
						self.reset()

				if self.game_state == GameStates.End:
					if event.key == pygame.K_SPACE:
						self.game_state = GameStates.Game
						self.reset()

		mouse_pressed = pygame.mouse.get_pressed()
		if self.game_state == GameStates.Game:
			if mouse_pressed[0]:
				if self.player.alive and self.player_shoot_timer.done():
					self.fire_sound.play()
					self.lasers.append(Laser(self.player.pos + get_angled_offset(self.player.image.angle, 25), self.player.image.angle))
					self.player_shoot_timer.start()

	def spawn_particles(self, amount_range, pos, radius, type, direction=None):
		amount = random.randint(amount_range[0], amount_range[1])
		for _ in range(amount):
			spawn_pos = pygame.Vector2(pos)
			spawn_pos += get_angled_offset(random.randint(0, 360), random.randint(0, radius))

			self.particles.append(Particle(type, spawn_pos, direction=direction))

	def spawn_asteroids(self):
		if self.asteroid_spawn_timer.done():
			for _ in range(random.randint(1, 3)):
				if self.player.input.length() == 0:
					pos = self.player.pos + get_angled_offset(random.randint(0, 360), 800)

					self.asteroids.append(Asteroid(AsteroidTypes.Large, pos, get_angle_to(pos, self.player.pos)))
				else:
					pos = self.player.pos + self.player.input.normalize().rotate(random.randint(-30, 30)) * 800

					self.asteroids.append(Asteroid(AsteroidTypes.Large, pos, get_angle_to(pos, self.player.pos)))

			self.asteroid_spawn_timer.time *= 0.95
			if self.asteroid_spawn_timer.time < 0.3:
				self.asteroid_spawn_timer.time = 3
			self.asteroid_spawn_timer.start()

	def game_update(self, delta):
		self.scroll = self.scroll.lerp(self.player.pos - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), min(0.07 * delta, 1))

		self.asteroid_spawn_timer.update(delta)
		self.death_timer.update(delta)

		if self.player.alive:
			self.spawn_asteroids()

			self.player_shoot_timer.update(delta)
			self.player_trail_timer.update(delta)
			self.player.update(delta, self.scroll)

			if self.player_trail_timer.done():
				self.spawn_particles(
					(2, 5),
					self.player.pos + get_angled_offset(self.player.image.angle + 180, self.player.radius),
					5,
					ParticleTypes.PlayerTrail,
					direction=get_angled_offset(self.player.image.angle + 180, 1)
				)
				self.player_trail_timer.start()

		# Update lists
		for laser in self.lasers[:]:
			laser.update(delta)

			if self.player.pos.distance_to(laser.pos) > 900:
				self.lasers.remove(laser)

		for asteroid in self.asteroids[:]:
			asteroid.update(delta)

			if self.player.pos.distance_to(asteroid.pos) > 900:
				self.asteroids.remove(asteroid)

		for particle in self.particles[:]:
			particle.update(delta)

			if particle.check_size():
				self.particles.remove(particle)

		# Check collisions
		for asteroid in self.asteroids[:]:
			for laser in self.lasers[:]:
				if asteroid.pos.distance_to(laser.pos) < asteroid.radius + laser.radius:
					self.lasers.remove(laser)
					self.laser_explosion_sound.play()

					self.spawn_particles((5, 8), laser.pos, laser.radius, ParticleTypes.Laser, direction=laser.movement)

					if asteroid.damage(5):
						self.asteroids.remove(asteroid)

						if asteroid.type == AsteroidTypes.Large:
							self.screen_shake = 0.15

							self.spawn_particles((60, 90), asteroid.pos, asteroid.radius, ParticleTypes.LargeAsteroid, direction=asteroid.movement)

							asteroid_dir = get_angle_to((0, 0), asteroid.movement)
							for _ in range(1, 3):
								self.asteroids.append(Asteroid(AsteroidTypes.Medium, asteroid.pos + get_angled_offset(random.randint(0, 360), random.randint(0, asteroid.radius)), asteroid_dir))

							self.score += 20
							self.large_asteroid_explosion_sound.play()

						elif asteroid.type == AsteroidTypes.Medium:
							self.screen_shake = 0.07

							self.spawn_particles((35, 60), asteroid.pos, asteroid.radius, ParticleTypes.MediumAsteroid, direction=asteroid.movement)

							self.score += 5
							self.medium_asteroid_explosion_sound.play()

		if self.player.alive:
			for asteroid in self.asteroids[:]:
				if self.player.pos.distance_to(asteroid.pos) < asteroid.radius + self.player.radius:
					if self.player.damage(asteroid.health):
						self.screen_shake = 5

						self.death_timer.start()

						self.spawn_particles((300, 400), self.player.pos, self.player.radius, ParticleTypes.PlayerExplosionBlast)

						for _ in range(random.randint(2, 3)):
							self.spawn_particles((60, 150), self.player.pos, self.player.radius, ParticleTypes.PlayerExplosionArm, direction=get_angled_offset(random.randint(0, 360), 1))

						self.player_explosion_sound.play()

					if asteroid.damage(self.player.health):
						self.asteroids.remove(asteroid)

						if asteroid.type == AsteroidTypes.Large:
							self.screen_shake = 0.15

							self.spawn_particles((60, 90), asteroid.pos, asteroid.radius, ParticleTypes.LargeAsteroid, direction=asteroid.movement)

							asteroid_dir = get_angle_to((0, 0), asteroid.movement)
							for _ in range(1, 3):
								self.asteroids.append(Asteroid(AsteroidTypes.Medium, asteroid.pos + get_angled_offset(random.randint(0, 360), random.randint(0, asteroid.radius)), asteroid_dir))

							self.large_asteroid_explosion_sound.play()

						elif asteroid.type == AsteroidTypes.Medium:
							self.screen_shake = 0.07

							self.spawn_particles((35, 60), asteroid.pos, asteroid.radius, ParticleTypes.MediumAsteroid, direction=asteroid.movement)

							self.medium_asteroid_explosion_sound.play()

		if not self.player.alive and self.death_timer.done() and len(self.asteroids) == 0:
			self.end_score_text.text = f"Score: {self.score}"
			self.game_state = GameStates.End

	def update(self):
		self.clock.tick()
		delta = self.clock.get_time() / 1000 * 60

		pygame.display.set_caption(f"Space Shooter: {round(self.clock.get_fps())}")

		self.screen_shake = max(0.0, self.screen_shake - delta / 60)

		for star in self.stars:
			star.update(delta, self.scroll)

		if self.game_state == GameStates.Start or self.game_state == GameStates.End:
			self.scroll.x += 3 * delta

		if self.game_state == GameStates.Game:
			self.game_update(delta)

	def draw(self):
		self.window.fill("black")

		scroll = self.scroll
		if self.screen_shake > 0:
			scroll += pygame.Vector2(random.randint(-4, 4), random.randint(-4, 4))

		for star in self.stars:
			star.draw(self.window, scroll)

		for laser in self.lasers:
			laser.draw(self.window, scroll)

		for asteroid in self.asteroids:
			asteroid.draw(self.window, scroll)

		for particle in self.particles:
			particle.draw(self.window, scroll)

		if self.game_state == GameStates.Start:
			self.start_text.draw_centered(self.window)

		if self.game_state == GameStates.Game:
			if self.player.alive:
				self.player.draw(self.window, scroll)

			self.score_text.text = f"{self.score}"
			self.score_text.draw_right(self.window)

			self.health_bar.draw(self.window, self.player.health, 100)

		if self.game_state == GameStates.End:
			self.end_score_text.draw_centered(self.window)
			self.end_restart_text.draw_centered(self.window)

		pygame.display.flip()
