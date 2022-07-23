from typing import Type

from data.modules.components.position import Position
from data.modules.game.game_object import GameObject
from data.modules.game.group import Group


def group_circle_collisions(group1: Group, group2: Group):
	collided_objects = {}
	for game_object1 in group1.objects:
		pos1: Position = game_object1.pos
		for game_object2 in group2.objects:
			pos2: Position = game_object2.pos

			if pos1.center.distance_to(pos2.center) < pos1.radius + pos2.radius:
				if game_object1 not in collided_objects:
					collided_objects[game_object1] = []

				collided_objects[game_object1].append(game_object2)

	return collided_objects


def single_group_circle_collisions(game_object: "GameObject", group: Group):
	collided_objects = []
	for game_object2 in group.objects:
		if game_object.pos.center.distance_to(game_object2.pos.center) < game_object.pos.radius + game_object2.pos.radius:
			collided_objects.append(game_object2)

	return collided_objects
