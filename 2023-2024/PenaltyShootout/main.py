import pygame
import math

from player import Player
from ball import Ball

screen = pygame.display.set_mode((600, 600))
clock = pygame.Clock()

player = Player()

ball = Ball((300, 400), (0, 0))

running = True
while running:
	clock.tick(60)
	pygame.display.set_caption(f"{round(clock.get_fps())}")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				angle = math.degrees(math.atan2(ball.pos.y - event.pos[1], ball.pos.x - event.pos[0])) - 90

				ball.shoot_ball(angle, 10)

	# Updating
	player.move()
	ball.update()

	# Drawing
	screen.fill("dark green")

	player.draw(screen)
	ball.draw(screen)

	pygame.display.flip()
