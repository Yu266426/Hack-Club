import pygame
from player import Player

pygame.init()

screen = pygame.display.set_mode((800, 800))

player = Player()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill("blue")

	player.draw(screen)

	pygame.display.update()

pygame.quit()
