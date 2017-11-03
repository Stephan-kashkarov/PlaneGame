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

	def events(self):
		keys = pg.get_keys()

		if keys[1]

	def run(self):
		self.events()
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
