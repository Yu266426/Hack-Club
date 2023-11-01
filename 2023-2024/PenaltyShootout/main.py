import pygame


class Player:
	def __init__(self):
		self.pos = pygame.Vector2((300, 300))

	def move(self):
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_d]:
			self.pos.x += 5
		if keys_pressed[pygame.K_a]:
			self.pos.x -= 5

		if self.pos.x - 20 < 0:
			self.pos.x = 20
		if self.pos.x + 20 > 600:
			self.pos.x = 600 - 20

	def draw(self, surface):
		pygame.draw.circle(surface, "white", self.pos, 20)


screen = pygame.display.set_mode((600, 600))
clock = pygame.Clock()

player = Player()

running = True
while running:
	clock.tick(60)
	pygame.display.set_caption(f"{round(clock.get_fps())}")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	player.move()

	screen.fill("dark green")

	player.draw(screen)

	pygame.display.flip()
