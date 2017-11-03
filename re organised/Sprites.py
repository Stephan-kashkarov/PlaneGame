class man:
	def __init__(self, x, y, sprite):
		self.x = x
		self.y = y
		self.rot = 0
		self.speed = PLAYERSPEED
		self.sprite = sprite

	def draw(self):
		pass

	def move(self):
		pass

	def run(self):
		self.move()
		self.draw()

class plane:
	def __init__(self, x, y, sprite):
		self.x = x
		self.y = y
		self.rot = 0
		self.speed = PLANESPEED
		self.sprite = sprite

	def draw(self):
		pass

	def move(self):
		pass

	def shoot(self):
		pass

	def run(self):
		self.move()
		self.draw()
