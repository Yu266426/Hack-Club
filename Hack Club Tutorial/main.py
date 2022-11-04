import pygame

from box import Box
from player import Player

pygame.init()  # Initializes pygame

window = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()

player = Player((250, 600))

box = Box()

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

	player.update()
	box.update()

	window.fill("light blue")  # Make the background blue

	box.draw(window)
	player.draw(window)

	pygame.display.update()  # Update our display to show changes

pygame.quit()
