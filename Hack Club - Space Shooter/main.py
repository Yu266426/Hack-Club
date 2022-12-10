import pygame

from data.modules.game import Game

pygame.init()

# Creates a game object, and calls the run method.
game = Game()
game.run()

pygame.quit()
