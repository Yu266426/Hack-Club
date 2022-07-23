import pygame


class BaseScene:
	def __init__(self):
		pass

	def handle_events(self, keys_pressed, mouse_pressed, mouse_pos, key_downs, key_ups):
		pass

	def update(self, delta: float):
		pass

	def draw(self, window: pygame.Surface):
		pass
