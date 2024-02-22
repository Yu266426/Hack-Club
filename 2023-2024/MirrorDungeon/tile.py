import pygame
import pygbase


class Tile:
	def __init__(self, pos: tuple, name: str, index: int, collidable: bool):
		self.rect = pygame.Rect(pos[0], pos[1], 16 * 5, 16 * 5)

		self.sprite_sheet: pygbase.SpriteSheet = pygbase.ResourceManager.get_resource("sprite_sheets", name)
		self.image = self.sprite_sheet.get_image(index)

		self.collidable = collidable

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.image.draw(surface, camera.world_to_screen(self.rect.topleft))


class TopWallTile(Tile):
	def __init__(self, pos: tuple, name: str, index: int, collidable: bool, top_sprite_index: int):
		super().__init__(pos, name, index, collidable)
		
		self.wall_top_sprite: pygbase.Image = pygbase.ResourceManager.get_resource("sprite_sheets", "wall_top").get_image(top_sprite_index)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		super().draw(surface, camera)
		self.wall_top_sprite.draw(surface, camera.world_to_screen((self.rect.left, self.rect.top - 4 * 5)))
