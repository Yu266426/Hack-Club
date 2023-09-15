class Timer:
	def __init__(self, time, start_on=True):
		self.time = time

		if start_on:
			self.timer = 0
		else:
			self.timer = time

	def done(self):
		return self.timer <= 0

	def start(self):
		self.timer = self.time

	def update(self, delta):
		self.timer -= delta / 60

		if self.timer < 0:
			self.timer = 0
