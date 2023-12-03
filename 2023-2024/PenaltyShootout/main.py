import pygame
import math

from goal import Goal
from goalie import Goalie
from player import Player
from ball import Ball

screen = pygame.display.set_mode((600, 600))
clock = pygame.Clock()

background_image = pygame.image.load("grass.png")

score = 0
goalie = Goalie(pygame.Rect(200, 400, 200, 40))
obstacles = [goalie.rect, pygame.Rect(40, 400, 30, 200), pygame.Rect(530, 400, 30, 200)]

goal = Goal((300, 500))

ball = Ball((300, 150), (0, 0))
is_in_goal = False

player = Player(ball.pos)

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
				angle = player.angle + 180

				ball.shoot_ball(angle, 10)

	# Updating
	player.update()
	ball.update(obstacles)
	goalie.update()

	# Ball is in goal
	if not is_in_goal and goal.rect.collidepoint(ball.pos):
		is_in_goal = True
		score += 1
		print(score)
	elif not goal.rect.collidepoint(ball.pos):
		is_in_goal = False

	# Drawing
	screen.fill("dark green")
	screen.blit(background_image, (-50, -40))

	player.draw(screen)
	ball.draw(screen)

	goal.draw(screen)

	for obstacle in obstacles:
		pygame.draw.rect(screen, "yellow", obstacle)

	pygame.display.flip()
