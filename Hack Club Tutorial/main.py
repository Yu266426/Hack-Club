import pygame

from box import Box
from player import Player

pygame.init()  # Initializes pygame

window = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()

player = Player((250, 600))

boxes = []
box_spawn_time = 0
box_cooldown = 30

# Game loop
is_running = True
while is_running:
	clock.tick(60)  # Keeps our game at 60 FPS

	for event in pygame.event.get():  # Loops through all events
		if event.type == pygame.QUIT:
			is_running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				is_running = False

			if event.key == pygame.K_SPACE:
				boxes.append(Box())

	box_spawn_time -= 1
	if box_spawn_time <= 0:
		boxes.append(Box())

		box_spawn_time = box_cooldown

		if box_cooldown > 5:
			box_cooldown *= 0.85

	player.update()

	for box in boxes:
		box.update()

		if box.rect.top > 800:
			boxes.remove(box)

	window.fill("light blue")  # Make the background blue

	for box in boxes:
		box.draw(window)

	player.draw(window)

	pygame.display.update()  # Update our display to show changes

pygame.quit()
