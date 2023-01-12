import pygame

from data.modules.laser import Laser
from data.modules.player import Player
from data.modules.timer import Timer


class Game:
	def __init__(self):
		self.is_running = True
		self.window = pygame.display.set_mode((800, 800))  # Sets the screen to 800 by 800 pixels
		self.clock = pygame.time.Clock()

		self.lasers = []

		self.player_shoot_timer = Timer(0.2)
		self.player = Player((400, 400))  # Initializes a player at 400, 400

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

	def update(self):
		# Limits FPS to 60
		self.clock.tick(60)

		self.player.update()

		if pygame.mouse.get_pressed(3)[0] and self.player_shoot_timer.update():
			self.lasers.append(Laser(self.player.pos, self.player.image.angle))

		for laser in self.lasers:
			laser.update()
			if not laser.image.get_rect(laser.pos).colliderect((0, 0, 800, 800)):
				self.lasers.remove(laser)

	def draw(self):
		self.window.fill((0, 0, 0))

		for laser in self.lasers:
			laser.draw(self.window)

		self.player.draw(self.window)

		pygame.display.update()

	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.draw()
