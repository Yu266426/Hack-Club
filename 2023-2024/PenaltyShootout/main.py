import pygame
import math

from goal import Goal
from player import Player
from ball import Ball

screen = pygame.display.set_mode((600, 600))
clock = pygame.Clock()

background_image = pygame.image.load("grass.png")

score = 0
obstacles = [pygame.Rect(200, 400, 200, 40)]

goal = Goal((300, 500))

player = Player()

ball = Ball((300, 350), (0, 0))
is_in_goal = False

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
	ball.update(obstacles)

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
