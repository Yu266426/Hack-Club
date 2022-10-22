import pygame

pygame.init()  # Initializes pygame

window = pygame.display.set_mode((800, 800))

# Game loop
is_running = True
while is_running:
	for event in pygame.event.get():  # Loops through all events
		if event.type == pygame.QUIT:
			is_running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				is_running = False

	window.fill("dark blue")  # Make the background blue

	pygame.display.update()  # Update our display to show changes

pygame.quit()
