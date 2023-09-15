from enum import Enum

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class GameStates(Enum):
	Start = 0
	Game = 1
	End = 2


class AsteroidTypes(Enum):
	Large = 0
	Medium = 1


class ParticleTypes(Enum):
	Laser = 0
	LargeAsteroid = 1
	MediumAsteroid = 2
	PlayerExplosionBlast = 3
	PlayerExplosionArm = 4
	PlayerTrail = 5
