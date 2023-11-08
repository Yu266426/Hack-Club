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


class Ball:
	def __init__(self, pos, velocity):
		self.pos = pygame.Vector2(pos)

		self.velocity = pygame.Vector2(velocity)

		self.image = pygame.image.load("soccer_ball.png")
		self.image = pygame.transform.scale(self.image, (40, 40))

		self.rect = self.image.get_rect(center=self.pos)

	def update(self):
		self.pos.x += self.velocity.x
		self.rect.center = self.pos

		if self.rect.left < 0:
			self.velocity.x *= -1
		if self.rect.right > 600:
			self.velocity.x *= -1

		self.pos.y += self.velocity.y
		self.rect.center = self.pos

		if self.rect.top < 0:
			self.velocity.y *= -1
		if self.rect.bottom > 600:
			self.velocity.y *= -1

	def draw(self, surface: pygame.Surface):
		surface.blit(self.image, self.rect)


screen = pygame.display.set_mode((600, 600))
clock = pygame.Clock()

player = Player()

ball = Ball((300, 400), (-2.4, 7.3))

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

	# Updating
	player.move()
	ball.update()

	# Drawing
	screen.fill("dark green")

	player.draw(screen)
	ball.draw(screen)

	pygame.display.flip()
