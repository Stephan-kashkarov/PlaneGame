import pygame as pg
import math
from settings import *
from functions import *

Kp = 0.007

class test:
	def __init__(self, x, y, screen):
		self.x = x
		self.y = y
		self.img = pg.draw.rect(self.screen, d_grey, (x, y, 10, 10))
		self.rect = img.get_rect()
		self.screen = screen

	def move(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.x -= 10
		elif keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.x += 10
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.y -= 10
		elif keys[pg.K_DOWN] or keys[pg.K_s]:
			self.y += 10

	def draw(self):
		self.screen.blit(self.img, (x,y))

	def run(self):
		self.move()
		self.draw()

class map_plane:
	def __init__(self, x, y, sprite, era, screen, camera):
		self.pos = [x, y]
		self.speed = [0, 0]
		self.rot = 0
		self.era = era
		self.camera = [x , y]

		if self.era == 0:
			self.speed = PLAYERSPEED_1
			self.sprite = pg.transform.scale(sprite[1], (20,20))
		if self.era == 1:
			self.speed = PLAYERSPEED_2
			self.sprite = pg.transform.scale(sprite[2], (20,20))
		if self.era == 2:
			self.speed = PLAYERSPEED_3
			self.sprite = pg.transform.scale(sprite[3], (20,20))
		self.rect = self.sprite.get_rect()
		self.alt = 0
		self.screen = screen

	def draw(self):
		self.rect = self.sprite.get_rect()
		rot_sprite = rot_center(self.sprite, self.rect, 270-self.rot)
		self.screen.blit(rot_sprite[0], (self.pos[0], self.pos[1]))

	def move(self):
		mouse_pos = pg.mouse.get_pos()

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

		# print("mouse_pos: ", mouse_pos, ", plane_pos: ", self.pos)

	def run(self):
		self.move()
		self.draw()

	def upgrade(self):
		if self.era < 3:
			self.era += 1

class battle_plane:
	def __init__(self, screen, x, y, sprite):
		self.pos = [x,y]
		self.rot = 0
		self.sprite = pg.transform.scale(sprite, (20,20))
		self.rect = self.sprite.get_rect()
		self.screen = screen
		self.era = 0
		self.rotation = 0
		self.throttle = 0
		self.energy = 1


	def draw(self):
		img = pg.transform.rotate(self.sprite, -self.rot)
		self.screen.blit(img, (self.pos[0], self.pos[1]))

	def events(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.rotation -= 1
		elif keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.rotation += 1
		if keys[pg.K_UP] or keys[pg.K_w]:
			if self.throttle < 100:
				self.throttle += 0.1
		elif keys[pg.K_DOWN] or keys[pg.K_s]:
			if self.throttle > 0:
				self.throttle -= 0.1

		if self.rotation <= 0:
			self.rotation = 360
		if self.rotation >= 360:
			self.rotation = 0

	def move(self):
		# Velocity
		if self.throttle > 1:
			self.throttle = 1
		if self.throttle < 0.2:
			self.throttle = 0.2
		if self.throttle >= 0.2 and self.throttle <= 1:
			self.speed = (((2.5 * math.sin(math.radians(self.rotation))) + 2) * self.throttle) * self.energy
			# Directional movement
			self.pos[0] += math.cos(math.radians(self.rotation)) * self.speed
			self.pos[1] += math.sin(math.radians(self.rotation)) * self.speed
			print("pos", self.pos, ", speed", self.speed, ", rotation", self.rotation)


	def run(self):
		self.events()
		self.move()
		self.draw()

	def upgrade(self):
		if self.era < 2:
			self.era += 1

class opponent:
	def __init__(self, screen, x, y, sprite):
		self.pos = [x,y]
		self.rot = 0
		self.sprite = pg.transform.scale(sprite, (20,20))
		self.rect = self.sprite.get_rect()
		self.screen = screen

	def draw(self):
		rot_sprite = rot_center(self.sprite, self.rect, self.rot)
		self.screen.blit(rot_sprite, (self.pos[0], self.pos[1]))

	def shoot(self):
		pass

