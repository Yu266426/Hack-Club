import os

import pygame

from files import ASSET_DIR

PLAYER_IMAGE = pygame.image.load(os.path.join(ASSET_DIR, "player.png"))
LASER_IMAGE = pygame.image.load(os.path.join(ASSET_DIR, "laser.png"))
