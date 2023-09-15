import math

import pygame


def get_angle_to(pos1, pos2):
	return math.degrees(math.atan2(pos1[1] - pos2[1], pos2[0] - pos1[0]))


def get_angled_offset(angle, offset):
	return pygame.Vector2(0, 1).rotate(-angle - 90) * offset
