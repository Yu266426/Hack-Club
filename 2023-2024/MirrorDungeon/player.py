import pygame
import pygbase


class Player:
	def __init__(self, pos: tuple):
		self.movement_speed = 500
		self.pos = pygame.Vector2(pos)

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheets", "player_idle", 0, 2), 2.0)
		], "idle")

	def update(self, delta: float):
		self.animations.update(delta)

		x_input = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.pos.x += x_input * self.movement_speed * delta

		y_input = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		self.pos.y += y_input * self.movement_speed * delta

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
