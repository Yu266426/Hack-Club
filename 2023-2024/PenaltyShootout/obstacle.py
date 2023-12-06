class Obstacle:
	def __init__(self, rect):
		self.rect = rect
		self.prev_rect = rect

	def update(self):
		pass


class Goalie(Obstacle):
	def __init__(self, rect):
		super().__init__(rect)

		self.direction = 1

	def update(self):
		self.prev_rect = self.rect.copy()
		self.rect.x += 10 * self.direction

		if self.rect.right > 600:
			self.direction = -1
		elif self.rect.left < 0:
			self.direction = 1
