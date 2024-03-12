import sys

import pygame
import pygbase

from editor import Editor
from files import ASSET_DIR
from game import Game

pygbase.init((800, 800))

# Load assets
pygbase.add_sprite_sheet_resource("sprite_sheets", 1, str(ASSET_DIR / "sprite_sheets"), default_scale=5)

# Quit when escape is pressed
pygbase.EventManager.add_handler("all", pygame.KEYDOWN, lambda e: pygbase.EventManager.post_event(pygame.QUIT) if e.key == pygame.K_ESCAPE else None)

args = sys.argv
print(args)
if len(args) == 1:
	print("Starting Game")
	app = pygbase.App(Game)
elif len(args) == 3 and args[1] == "-e":
	print(f"Starting Editor: {args[2]}")
	pygbase.Common.set_value("level_name", args[2])
	app = pygbase.App(Editor)
else:
	app = pygbase.App(Game)
app.run()

pygbase.quit()
