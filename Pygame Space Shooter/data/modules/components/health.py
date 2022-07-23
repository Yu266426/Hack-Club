from data.modules.components.damage import Damage


class Health:
	def __init__(self, health: int):
		self.health = health

	def damage(self, damage: Damage):
		self.health -= damage.damage

	def check_alive(self):
		return 0 < self.health
