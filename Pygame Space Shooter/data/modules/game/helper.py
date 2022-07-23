import math
import random

import pygame


def get_angle_to(pos: tuple[int | float, int | float] | pygame.Vector2, to: tuple[int | float, int | float] | pygame.Vector2) -> float:
	# Gets the relative angle
	return math.degrees(math.atan2(pos[1] - to[1], to[0] - pos[0]))


def create_coloured_surface(size: tuple[int, int], colour: tuple[int, int, int] | str) -> pygame.Surface:
	surface = pygame.Surface(size)
	surface.fill(colour)

	return surface


def get_angled_offset(angle, amount) -> pygame.Vector2:
	return pygame.math.Vector2(math.cos(math.radians(angle)) * amount, -1 * math.sin(math.radians(angle)) * amount)


def get_random_float(range_min: int | float, range_max: int | float) -> float:
	return random.randint(int(range_min * 100), int(range_max * 100)) / 100.0
