import os.path

import pygame.display

from data.modules.files import ASSETS_PATH


class Game:
	def __init__(self):
		self.is_running = True

		self.window = pygame.display.set_mode((800, 800))
		self.clock = pygame.time.Clock()

		self.angle = 0

		self.base_image = pygame.image.load(os.path.join(ASSETS_PATH, "large asteroid.png"))
		self.base_image = pygame.transform.scale(self.base_image, (self.base_image.get_width() * 5, self.base_image.get_height() * 5))
		self.base_rect = self.base_image.get_rect(topleft=(300, 300))

		self.image = self.base_image.copy()
		self.rect = self.image.get_rect(center=self.base_rect.center)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

	def update(self):
		self.clock.tick(60)

		self.angle += 0.5

		self.image = pygame.transform.rotate(self.base_image, self.angle)
		self.rect = self.image.get_rect(center=self.base_rect.center)

	def draw(self):
		self.window.fill("black")

		self.window.blit(self.image, self.rect)

		pygame.display.update()
