import pathlib
import random

import pygame

from large_asteroid import LargeAsteroid
from laser import Laser
from particle import Particle
from player import Player

current_dir = pathlib.Path.cwd()
asset_dir = current_dir / "assets"


def load_image(name: str, scale: float):
	return pygame.transform.scale_by(pygame.image.load(asset_dir / name).convert_alpha(), scale)


screen = pygame.display.set_mode((600, 800), flags=pygame.SCALED, vsync=True)
pygame.display.set_caption("Hack Club!")
clock = pygame.Clock()

player_image = load_image("player.png", 4)
laser_image = load_image("laser.png", 3)
large_asteroid_image = load_image("large asteroid.png", 3)

player = Player(player_image, (300, 670))

lasers = []
laser_cooldown = 0.2
laser_timer = 0.0
laser_damage = 5

asteroids = []
asteroid_spawn_cooldown = 0
asteroid_timer = asteroid_spawn_cooldown

particles = []
laser_particle_colours = ["yellow", "orange"]
asteroid_particle_colours = [(209, 98, 0), (207, 34, 14), (214, 93, 17)]

running = True
while running:
	delta = clock.tick() / 1000
	laser_timer -= delta
	asteroid_timer -= delta

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

			if event.key == pygame.K_f:
				asteroids.append(LargeAsteroid(large_asteroid_image, (300, 100)))

	keys_pressed = pygame.key.get_pressed()

	if asteroid_timer <= 0.0:
		asteroids.append(LargeAsteroid(large_asteroid_image, (random.uniform(player.pos.x - 40, player.pos.x + 40) % 600, -200)))

		asteroid_timer = asteroid_spawn_cooldown

		asteroid_spawn_cooldown *= 0.80
		if asteroid_spawn_cooldown <= 0.3:
			asteroid_spawn_cooldown = 0.5

	if laser_timer <= 0.0 and keys_pressed[pygame.K_SPACE]:
		lasers.append(Laser(laser_image, player.pos))

		laser_timer = laser_cooldown

	player.update(delta)

	for particle in particles.copy():
		particle.update(delta)
		if particle.size < 2:
			particles.remove(particle)

	for laser in lasers.copy():
		laser.update(delta)

		if laser.rect.bottom < 0:
			lasers.remove(laser)
			continue

		for asteroid in asteroids:
			if laser.pos.distance_to(asteroid.pos) < asteroid.rect.width * 0.45:
				asteroid.health -= laser_damage

				for _ in range(random.randint(4, 12)):
					initial_velocity = pygame.Vector2(0, -1).rotate(random.uniform(-30, 30)) * random.uniform(70, 200)
					particles.append(Particle(laser.pos, initial_velocity, random.choice(laser_particle_colours), random.uniform(4, 8)))

				lasers.remove(laser)
				break

	for asteroid in asteroids.copy():
		asteroid.update(delta)

		if asteroid.rect.top > 800:
			asteroids.remove(asteroid)

		elif asteroid.health <= 0:
			for _ in range(random.randint(40, 120)):
				initial_velocity = pygame.Vector2(0, 1).rotate(random.uniform(0, 360)) + pygame.Vector2(0, 0.7)
				initial_velocity = initial_velocity.normalize() * random.uniform(asteroid.speed - 20, asteroid.speed + 20)

				particles.append(Particle(
					asteroid.pos + initial_velocity.normalize() * random.uniform(0, asteroid.rect.width / 2),
					initial_velocity,
					random.choice(asteroid_particle_colours),
					random.uniform(6, 9)
				))

			asteroids.remove(asteroid)

	screen.fill("black")

	for laser in lasers:
		laser.draw(screen)

	for asteroid in asteroids:
		asteroid.draw(screen)

	for particle in particles:
		particle.draw(screen)

	player.draw(screen)

	pygame.display.flip()
