class Timer:
	def __init__(self, cooldown):
		self.cooldown = cooldown

		self.time = self.cooldown

	def update(self):
		self.time -= 1 / 60
		if self.time < 0:
			self.time = self.cooldown
			return Timer
		return False
