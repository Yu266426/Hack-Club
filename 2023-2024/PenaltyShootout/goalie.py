class Goalie:
	def __init__(self, rect):
		self.rect = rect

		self.direction = 1

	def update(self):
		self.rect.x += 10 * self.direction

		if self.rect.right > 600:
			self.direction = -1
		elif self.rect.left < 0:
			self.direction = 1
