# Import pygame tells our file that we are using pygame
import random

import pygame

# Imports our classes we made
from box import Box
from player import Player

# ------------------------------------ Initialization ---------------------------------
# Initializes pygame.
# Pygame handles a lot of complicated stuff in the background, and this allows it to set up everything it needs.
pygame.init()

# ----------------------------------- Setup  ---------------------------------
# Creates a window with the size 500 by 800 pixels
window = pygame.display.set_mode((500, 800))

# Creates a clock, which will be used to set our framerate
clock = pygame.time.Clock()

# -------------------------------- Game Objects ---------------------------------
# We make a new player here
player = Player((250, 700), (20, 50))

boxes = []
box_spawn_timer = 0
box_spawn_cooldown = 0.5


# --------------------------- Functions ---------------------------------------
def spawn_box():
	boxes.append(Box(
		(random.randint(0, window.get_width()), -50)
	))


# --------------------------------------- Game Loop --------------------------------
# Our main game loop, runs only when "running" is true
running = True
while running:
	# Limits our framerate to 60 FPS
	clock.tick(60)

	# --------------------------- Events ---------------------------------
	# Main event loop.
	# This makes sure that pygame is taking in events, like buttons being clicked, or the X button to quit the game
	for event in pygame.event.get():
		# Checks if the type of the event is pygame.QUIT,
		# which is when you press the X button to close an application
		if event.type == pygame.QUIT:
			# Set running to False, which ends our game loop
			running = False

		# If a key is pressed down
		if event.type == pygame.KEYDOWN:
			# If the key is escape, quit the game
			if event.key == pygame.K_ESCAPE:
				running = False

	# -------------------------- Updates ---------------------------------
	# Spawns in boxes if it can, otherwise count down the time
	if box_spawn_timer <= 0:
		spawn_box()
		box_spawn_timer = box_spawn_cooldown

		box_spawn_cooldown *= 0.95
		if box_spawn_cooldown < 0.08:
			box_spawn_cooldown = 0.08
	else:
		box_spawn_timer -= clock.get_time() / 1000

	# Updates our player
	player.update()

	# Updates boxes
	for box in boxes:
		box.update()

	# -------------------------- Drawing ---------------------------------
	# Fills the background with "light blue"
	window.fill("light blue")

	# Draws out player in front of the background
	player.draw()

	# Draws boxes
	for box in boxes:
		box.draw()

	# Updates our display, to make sure everything we draw shows up
	pygame.display.update()

pygame.quit()
