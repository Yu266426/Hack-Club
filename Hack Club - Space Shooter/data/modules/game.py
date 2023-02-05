import pygame

from data.modules.player import Player


class Game:
	def __init__(self):
		self.is_running = True
		self.window = pygame.display.set_mode((800, 800))  # Sets the screen to 800 by 800 pixels
		self.clock = pygame.time.Clock()

		self.player = Player((400, 400))  # Initializes a player at 400, 400

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

	def update(self):
		# Limits FPS to 60
		self.clock.tick(60)

		self.player.update()

	def draw(self):
		self.window.fill((0, 0, 0))

		self.player.draw(self.window)

		pygame.display.update()

	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.draw()
