import pygame as pg
import math

Kp = 0.004

class map_plane:
	def __init__(self, x, y, sprite, fps, era):
		self.pos = [x, y]
		self.speed = [0, 0]
		self.rot = 0
		self.era = era
		if self.era == 0:
			self.speed = PLAYERSPEED_1
			self.sprite = sprite[1]
		if self.era == 1:
			self.speed = PLAYERSPEED_2
			self.sprite = sprite[2]
		if self.era == 2:
			self.speed = PLAYERSPEED_3
			self.sprite = sprite[3]
		self.alt = 0

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

class battle_plane:
	def __init__(self, screen, x, y, sprite):
		self.pos = [x,y]
		self.rot = 0
		self.sprite = sprite
		self.screen = screen

	def draw(self):
		img = pg.transform.rotate(self.sprite, -self.rot)
		self.screen.blit(img, (self.pos[0], self.pos[1]))

	def move(self):
		mouse_pos = pg.mouse.get_pos();
		# Plane rotation
		run = mouse_pos[0]-self.pos[0]
		rise = mouse_pos[1]-self.pos[1]
		if run == 0:
			run = 1
		gradient = rise/run

		#print(gradient)
		self.rot = math.degrees(math.atan(gradient))
		if run <= 0:
			if rise > 0:
				self.rot = -180 + self.rot
			else:
				self.rot = 180 + self.rot

		# New plane position
		for i in range(0,2):
		 	self.pos[i] += Kp*(mouse_pos[i] - self.pos[i])

	def shoot(self):
		pass

	def run(self):
		self.move()
		self.draw()
