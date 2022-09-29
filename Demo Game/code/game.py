import json
import random

import pygame

from box import Box
from file import LEADERBOARD_PATH
from player import Player
from textbox import TextBox


class Game:
	def __init__(self):
		self.is_running = True

		self.window = pygame.display.set_mode((540, 850), flags=pygame.SCALED | pygame.FULLSCREEN, vsync=1)
		pygame.display.set_caption("Demo Game!")

		self.clock = pygame.time.Clock()

		self.game_state = "start"

		self.game_time = 0

		self.large_font = pygame.font.SysFont("arial", 50, bold=True)
		self.medium_font = pygame.font.SysFont("arial", 30, bold=True)
		self.start_text = self.large_font.render("Press Space To Start!", True, (5, 68, 94))

		self.player = Player((self.window.get_width() / 2, 700), (20, 50))

		self.boxes: list[Box] = []
		self.box_spawn_timer = 0
		self.box_spawn_cooldown = 0.5

		self.text_active = False

		self.name_input_text = self.medium_font.render("Type in your name! Eg. Tiger Zhang", True, (5, 68, 94))
		self.text_input = TextBox((self.window.get_width() / 2, 500), (400, 50))

	def spawn_box(self):
		self.boxes.append(Box(
			(random.randint(0, self.window.get_width()), -50)
		))

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.is_running = False

			if self.game_state == "start":
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.game_state = "game"

						self.boxes.clear()
						self.box_spawn_cooldown = 0.5

						self.player.pos.x = self.window.get_width() / 2

						self.game_time = 0

			elif self.game_state == "end":
				if event.type == pygame.KEYDOWN:
					if self.text_input.write(event, pygame.time.get_ticks()):
						# Save info
						with open(LEADERBOARD_PATH) as file:
							data = json.load(file)

						name = self.text_input.text.lower().strip()
						time = round(self.game_time, 2)

						if name in data:
							time = max(time, data[name])

						data[name] = time

						with open(LEADERBOARD_PATH, "w") as file:
							file.write(json.dumps(data))

						# Reset
						self.game_state = "start"

						self.boxes.clear()
						self.box_spawn_cooldown = 0.5
						self.text_input.text = ""
						self.text_input.selected = False

					if pygame.key.get_mods() & pygame.KMOD_CTRL and event.key == pygame.K_SPACE:
						self.game_state = "start"

						self.boxes.clear()
						self.box_spawn_cooldown = 0.5

						self.text_input.text = ""
						self.text_input.selected = False

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
					self.text_input.selected = True

		if self.game_state == "game":
			self.game_time += delta / 60

			self.player.update(delta)

		if self.game_state == "end":
			self.text_input.update()

			self.text_active = self.text_input.selected

	def draw(self):
		self.window.fill((173, 216, 230))

		if self.game_state == "start":
			for box in self.boxes:
				box.draw()

			self.window.blit(self.start_text, (self.window.get_width() / 2 - self.start_text.get_width() / 2, 150))

		elif self.game_state == "game":
			self.player.draw()

			# Draws boxes
			for box in self.boxes:
				box.draw()

			rendered_time = self.large_font.render(f"{round(self.game_time, ndigits=2)}", True, (5, 68, 94))
			self.window.blit(rendered_time, (10, 10))

		elif self.game_state == "end":
			end_text = self.large_font.render(f"Your score was {round(self.game_time)}!", True, (5, 68, 94))
			self.window.blit(end_text, (self.window.get_width() / 2 - end_text.get_width() / 2, 150))

			self.window.blit(self.name_input_text, (self.window.get_width() / 2 - self.name_input_text.get_width() / 2, 400))
			self.text_input.draw(self.window)

		# Updates our display, to make sure everything we draw shows up
		pygame.display.update()
