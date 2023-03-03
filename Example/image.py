import pygame


class Image:
	def __init__(self, image: pygame.Surface, size, angle=0):
		self.image = pygame.transform.scale(image.convert_alpha(), size)
		self.angle = angle

	def get_rect(self, pos):
		return self.image.get_rect(center=pos)

	def draw(self, screen, rect):
		rotated_image = pygame.transform.rotate(self.image, self.angle)
		screen.blit(rotated_image, rotated_image.get_rect(center=rect.center))
