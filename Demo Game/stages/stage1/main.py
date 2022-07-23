# Import pygame tells our file that we are using pygame
import pygame

# ------------------------------------ Initialization ---------------------------------
# Initializes pygame.
# Pygame handles a lot of complicated stuff in the background, and this allows it to set up everything it needs.
pygame.init()

# ----------------------------------- Setup  ---------------------------------
# Creates a window with the size 500 by 800 pixels
window = pygame.display.set_mode((500, 800))

# Creates a clock, which will be used to set our framerate
clock = pygame.time.Clock()

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

	# -------------------------- Drawing ---------------------------------
	# Fills the background with "light blue"
	window.fill("light blue")

	# Updates our display, to make sure everything we draw shows up
	pygame.display.update()
