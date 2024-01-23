import pygame

import images

display = pygame.display.set_mode((800, 800))

images.load_image("tileset")

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	display.fill("blue")
	display.blit(images.images["tileset"], (0, 0))

	pygame.display.update()
