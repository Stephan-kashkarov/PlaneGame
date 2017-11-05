import pygame as pg

Kp = 0.004

class man:
	def __init__(self, x, y, sprite, fps):
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
		self.vx, self.vy = 0, 0
		keys = pg.key.get_pressed()


		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel.x = -player_speed
		elif keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel.x = player_speed
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel.y = -player_speed
		elif keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel.y = player_speed

		if self.vel.x != 0 and self.vel.y !=0:
			self.vel *= 0.7071


	def run(self):
		self.events()
		self.move()
		self.draw()

class plane:
	def __init__(self, screen, x, y, sprite):
		self.pos = [x,y]
		self.sprite = sprite
		self.screen = screen

	def draw(self):
		self.screen.blit(self.sprite, (self.pos[0], self.pos[1]))

	def move(self):
		mouse_pos = pg.mouse.get_pos();
		for i in range(0,2):
			self.pos[i] += Kp*(mouse_pos[i] - self.pos[i])

	def shoot(self):
		pass

	def run(self):
		self.move()
		self.draw()
