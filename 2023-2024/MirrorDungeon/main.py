import pathlib

import pygame
import pygbase

from game import Game

pygbase.init((800, 800))

# Load assets
CURRENT_DIR = pathlib.Path.cwd()
ASSET_DIR = CURRENT_DIR / "assets"

pygbase.add_sprite_sheet_resource("sprite_sheets", 1, str(ASSET_DIR / "sprite_sheets"), default_scale=5)

# Quit when escape is pressed
pygbase.EventManager.add_handler(
    "all", pygame.KEYDOWN, lambda e: pygbase.EventManager.post_event(pygame.QUIT) if e.key == pygame.K_ESCAPE else None)

app = pygbase.App(Game)
app.run()

pygbase.quit()
