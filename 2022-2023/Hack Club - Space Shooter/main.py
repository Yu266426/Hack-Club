import pygame

from data.modules.game import Game

# Initializes pygame, to set up things that pygame needs
pygame.init()

# Creates a game object, and calls the run method.
game = Game()
game.run()

# Quits pygame
pygame.quit()
