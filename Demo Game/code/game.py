import random

import pygame

from box import Box
from player import Player


class Game:
	def __init__(self):
		self.is_running = True

		self.window = pygame.display.set_mode((500, 800))
		pygame.display.set_caption("Demo Game!")

		self.clock = pygame.time.Clock()

		self.game_state = "start"

		self.game_time = 0

		self.font = pygame.font.SysFont("arial", 50, bold=True)
		self.start_text = self.font.render("Press Space To Start!", True, "white")

		self.player = Player((self.window.get_width() / 2, 700), (20, 50))

		self.boxes: list[Box] = []
		self.box_spawn_timer = 0
		self.box_spawn_cooldown = 0.5

	def spawn_box(self):
		self.boxes.append(Box(
			(random.randint(0, self.window.get_width()), -50)
		))

	def handle_events(self):
		for event in pygame.event.get():
			# Checks if the type of the event is pygame.QUIT,
			# which is when you press the X button to close an application
			if event.type == pygame.QUIT:
				# Set running to False, which ends our game loop
				self.is_running = False

			# If a key is pressed down
			if event.type == pygame.KEYDOWN:
				# If the key is escape, quit the game
				if event.key == pygame.K_ESCAPE:
					self.is_running = False

				if self.game_state == "start" and event.key == pygame.K_SPACE:
					self.game_state = "game"

					self.boxes.clear()
					self.box_spawn_cooldown = 0.5

					self.player.pos.x = self.window.get_width() / 2

					self.game_time = 0

				elif self.game_state == "end" and event.key == pygame.K_SPACE:
					self.game_state = "start"

					self.boxes.clear()
					self.box_spawn_cooldown = 0.5

	def update(self):
		self.clock.tick()
		delta = self.clock.get_time() / 1000 * 60

		if self.box_spawn_timer <= 0:
			self.spawn_box()
			self.box_spawn_timer = self.box_spawn_cooldown

			self.box_spawn_cooldown *= 0.95
			if self.box_spawn_cooldown < 0.08:
				self.box_spawn_cooldown = 0.08
		else:
			self.box_spawn_timer -= delta / 60

		# Updates boxes
		for box in self.boxes:
			box.update(delta)

			if self.game_state == "game":
				if box.rect.collidepoint(self.player.rect.centerx, self.player.rect.centery):
					self.game_state = "end"

		if self.game_state == "game":
			self.game_time += delta / 60

			# Updates our player
			self.player.update(delta)

	def draw(self):
		self.window.fill("light blue")

		if self.game_state == "start":
			# Draws boxes
			for box in self.boxes:
				box.draw()

			self.window.blit(self.start_text, (self.window.get_width() / 2 - self.start_text.get_width() / 2, 150))
		elif self.game_state == "game":
			# Draws out player in front of the background
			self.player.draw()

			# Draws boxes
			for box in self.boxes:
				box.draw()

			rendered_time = self.font.render(f"{round(self.game_time, ndigits=2)}", True, "white")
			self.window.blit(rendered_time, (10, 10))
		elif self.game_state == "end":
			end_text = self.font.render(f"Your score was {round(self.game_time)}!", True, "white")
			self.window.blit(end_text, (self.window.get_width() / 2 - end_text.get_width() / 2, 150))

		# Updates our display, to make sure everything we draw shows up
		pygame.display.update()
