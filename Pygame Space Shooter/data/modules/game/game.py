import pygame

from data.modules.game.contants import WINDOW_SIZE
from data.modules.game.events import PLAYER_DEATH
from data.modules.game.image_loader import ImageLoader
from data.modules.scenes.game_scene import GameScene


class Game:
	def __init__(self):
		# Load game
		self.is_running = True
		self.window = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)
		pygame.display.set_caption("Space Shooter")
		self.clock = pygame.time.Clock()

		ImageLoader.load_images()

		self.game_scene = GameScene()

		self.scene = self.game_scene

	def handle_events(self):
		# Get inputs
		keys_pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed(3)
		mouse_pos = pygame.mouse.get_pos()

		key_downs = list()
		key_ups = list()

		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

			if event.type == PLAYER_DEATH:
				self.is_running = False

			if event.type == pygame.KEYDOWN:
				key_downs.append(event.key)

				if event.key == pygame.K_ESCAPE:
					self.is_running = False

			if event.type == pygame.KEYUP:
				key_ups.append(event.key)

		self.scene.handle_events(keys_pressed, mouse_pressed, mouse_pos, key_downs, key_ups)

	def update(self):
		# Tick the clock / Calculate delta
		self.clock.tick()
		delta = self.clock.get_time() * 0.001 * 60

		pygame.display.set_caption(f"Space Shooter ({round(self.clock.get_fps())})")

		self.scene.update(delta)

	def draw(self):
		self.scene.draw(self.window)

		# Update display
		pygame.display.update()
