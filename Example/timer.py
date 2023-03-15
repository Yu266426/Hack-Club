class Timer:
	def __init__(self, time, start_on):
		self.time = time

		self.timer = 0 if start_on else time

	def start_timer(self):
		self.timer = self.time

	def update(self, delta_time=1 / 60):
		self.timer -= delta_time

		if self.timer <= 0:
			return True
		else:
			return
