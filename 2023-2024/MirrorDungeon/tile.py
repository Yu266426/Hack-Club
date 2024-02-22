import pygame
import pygbase


class Tile:
<<<<<<< Updated upstream
	def __init__(self, pos, name, index, collidable):
=======
	def __init__(self, pos: tuple, name: str, index: int, collidable: bool):
>>>>>>> Stashed changes
		self.rect = pygame.Rect(pos[0], pos[1], 16 * 5, 16 * 5)

		self.sprite_sheet: pygbase.SpriteSheet = pygbase.ResourceManager.get_resource("sprite_sheets", name)
		self.image = self.sprite_sheet.get_image(index)

		self.collidable = collidable

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.image.draw(surface, camera.world_to_screen(self.rect.topleft))
