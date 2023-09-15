import pygame

from laser import Laser
from player import Player
from timer import Timer

screen = pygame.display.set_mode((800, 800))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()

player = Player()

laser_cooldown = Timer(0.1, True)
lasers = []

running = True
while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	mouse_pressed = pygame.mouse.get_pressed()

	# Updates
	player.update()

	if mouse_pressed[0] and laser_cooldown.update():
		lasers.append(Laser(player.pos, player.image.angle))
		laser_cooldown.start_timer()

	for laser in lasers:
		laser.update()

		if not screen_rect.contains(laser.rect):
			lasers.remove(laser)

	# Drawing
	screen.fill("black")

	for laser in lasers:
		laser.draw(screen)

	player.draw(screen)

	pygame.display.update()
