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

# Time passed in game
game_time = 0

# Game state controls what is happening in our game
game_state = "start"

# ---------------------------- Fonts ------------------------------
font = pygame.font.SysFont("arial", 50, bold=True)

start_text = font.render("Press Space To Start!", True, "white")

# -------------------------------- Game Objects ---------------------------------
# We make a new player here
player = Player((250, 700), (20, 50))

boxes: list[Box] = []
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

			if game_state == "start" and event.key == pygame.K_SPACE:
				game_state = "game"

				boxes.clear()
				box_spawn_cooldown = 0.5

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

	# Updates boxes
	for box in boxes:
		box.update()

		if game_state == "game":
			if box.rect.collidepoint(player.rect.centerx, player.rect.centery):
				game_state = "end"

	if game_state == "game":
		game_time += clock.get_time() / 1000

		# Updates our player
		player.update()

	# -------------------------- Drawing ---------------------------------
	# Fills the background with "light blue"
	window.fill("light blue")

	if game_state == "start":
		# Draws boxes
		for box in boxes:
			box.draw()

		window.blit(start_text, (250 - start_text.get_width() / 2, 150))
	elif game_state == "game":
		# Draws out player in front of the background
		player.draw()

		# Draws boxes
		for box in boxes:
			box.draw()

		rendered_time = font.render(f"{round(game_time, ndigits=2)}", True, "white")
		window.blit(rendered_time, (10, 10))
	elif game_state == "end":
		end_text = font.render(f"Your score was {round(game_time)}!", True, "white")
		window.blit(end_text, (250 - end_text.get_width() / 2, 150))

	# Updates our display, to make sure everything we draw shows up
	pygame.display.update()

pygame.quit()
