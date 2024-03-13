import logging
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
num_args = len(args) - 1
print(args)

if num_args == 0:  # Start game, no args
	print("Starting Game")
	pygbase.Common.set_value("level_name", "test")
	app = pygbase.App(Game)
elif num_args == 1:  # Start game, level name
	pygbase.Common.set_value("level_name", args[1])
	app = pygbase.App(Game)
elif num_args == 2 and args[1] == "-e":  # Start editor, level name
	print(f"Starting Editor: {args[2]}")
	pygbase.Common.set_value("level_name", args[2])
	pygbase.Common.set_value("level_size", (10, 10))
	app = pygbase.App(Editor)
elif num_args == 4 and args[1] == "-e":  # Start editor, level name, level size
	try:
		num_cols = int(args[3])
		num_rows = int(args[4])
	except ValueError:
		logging.error("Provided arguments 3 and 4 do not convert to integers")
		raise ValueError("Provided arguments 3 and 4 do not convert to integers")

	pygbase.Common.set_value("level_name", args[2])
	pygbase.Common.set_value("level_size", (num_cols, num_rows))
	app = pygbase.App(Editor)
else:
	logging.error(f"Invalid startup arguments: {args=}")
	raise ValueError(f"Invalid startup arguments: {args=}")

app.run()

pygbase.quit()
