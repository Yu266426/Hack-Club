import pygame

from box import Box
from player import Player

pygame.init()  # Initializes pygame

window = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()

game_state = "game"

player = Player((250, 600))

boxes = []
box_spawn_time = 0
box_cooldown = 30

font = pygame.font.SysFont("arial", 70)  # Loads the font
end_text = font.render("Game Over!", True, "white")  # "renders" font into an image <Surface>
score_text = font.render("0", True, "white")

time_text = font.render("0", True, "white")

restart_time = 0  # Subtracts from the current time so that 0 is the time at the start of the game

# Game loop
is_running = True
while is_running:
	clock.tick(60)  # Keeps our game at 60 FPS

	for event in pygame.event.get():  # Loops through all events
		if event.type == pygame.QUIT:
			is_running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				is_running = False

			if event.key == pygame.K_SPACE:
				if game_state == "end":
					game_state = "restart"
					restart_time = pygame.time.get_ticks() / 1000

	if game_state == "game":
		# Box spawning
		box_spawn_time -= 1
		if box_spawn_time <= 0:
			boxes.append(Box())

			box_spawn_time = box_cooldown

			if box_cooldown > 5:
				box_cooldown *= 0.85

		player.update()

		# Box updating
		for box in boxes:
			box.update()

			# If box collides with the middle top of the player
			if box.rect.collidepoint(player.rect.midtop):
				end_time = round(pygame.time.get_ticks() / 1000 - restart_time)
				score_text = font.render(f"You Got {end_time}!", True, "white")

				game_state = "end"
				break  # Breaks out of for loop, as no further boxes need to be processed

			if box.rect.top > 800:
				boxes.remove(box)

		# Updates the timer displayed to the player
		time_text = font.render(f"{round(pygame.time.get_ticks() / 1000 - restart_time, 1)}", True, "white")

	elif game_state == "restart":
		boxes.clear()
		box_spawn_time = 0
		box_cooldown = 30

		player = Player((250, 600))

		end_time = 0

		game_state = "game"

	window.fill("light blue")  # Make the background blue

	if game_state == "game":
		for box in boxes:
			box.draw(window)

		player.draw(window)

		window.blit(time_text, (20, 20))

	if game_state == "end":
		window.blit(end_text, (250 - end_text.get_width() / 2, 200))
		window.blit(score_text, (250 - score_text.get_width() / 2, 300))

	pygame.display.update()  # Update our display to show changes

pygame.quit()
