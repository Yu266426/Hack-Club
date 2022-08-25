import pygame

from data.modules.game import Game

pygame.init()

game = Game()
while game.is_running:
	game.handle_events()
	game.update()
	game.draw()

pygame.quit()
