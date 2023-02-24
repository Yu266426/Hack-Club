import pygame

from player import Player

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

player = Player()

running = True
while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	# Updates
	player.update()

	# Drawing
	screen.fill("black")

	player.draw(screen)

	pygame.display.update()
