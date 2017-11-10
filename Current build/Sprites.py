import pygame as pg
import math
import random
from settings import *
from functions import *

Kp = 0.01

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
	def __init__(self, x, y, sprite, era, screen):
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

	def collision(self, x, y, camera_pos):
		playerx = camera_pos[0] + display_width/2
		playery = camera_pos[1] + display_height/2

		if playerx <= x + 60 and playerx >= x:
			if playery <= y + 30 and playery >= y:
				print("collision")
				return True

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
		self.energy = 4


	def draw(self):
		new_img = rot_center(self.sprite, self.rect, 270-self.rotation)
		self.screen.blit(new_img[0], (self.pos[0], self.pos[1]))

	def events(self):
		keys = pg.key.get_pressed()
		mouse_pos = pg.mouse.get_pos()

		# Plane rotation
		run = mouse_pos[0]-self.pos[0]
		rise = mouse_pos[1]-self.pos[1]
		if run == 0:
			run = 1
		gradient = rise/run

		#print(gradient)
		self.rotation = math.degrees(math.atan(gradient))
		if run <= 0:
			if rise > 0:
				self.rotation = -180 + self.rotation
			else:
				self.rotation = 180 + self.rotation
		if keys[pg.K_UP] or keys[pg.K_w]:
			if self.throttle < 100:
				self.throttle += 0.1
		elif keys[pg.K_DOWN] or keys[pg.K_s]:
			if self.throttle > 0:
				self.throttle -= 0.1

	def move(self):
		# Velocity
		if self.pos[1] >= display_height - 100:
			return True
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

	def upgrade(self):
		if self.era < 2:
			self.era += 1

class map_opponent:
	def __init__(self, sprite, era, screen, camera_size, map_size):
		self.pos_on_map = [random.randint(0, map_size[0]), random.randint(0, map_size[1])]
		self.rot = 0
		self.era = era
		self.camera_size = camera_size
		self.map_size = map_size
		self.num_steps = fps*random.randint(3, 30)	# this is how many steps it will take to reach the player
		self.step_count = 0
		self.draw_me = False
		self.pos_on_screen = [0,0]

		print("NumSteps: ", self.num_steps, "Seconds: ", self.num_steps/fps, "good luck running!")

		if self.era == 0:
			self.sprite = pg.transform.scale(sprite[1], (20,20))
		if self.era == 1:
			self.sprite = pg.transform.scale(sprite[2], (20,20))
		if self.era == 2:
			self.sprite = pg.transform.scale(sprite[3], (20,20))
		self.rect = self.sprite.get_rect()
		self.alt = 0
		self.screen = screen

	def draw(self):
		if self.draw_me:
			self.rect = self.sprite.get_rect()
			rot_sprite = rot_center(self.sprite, self.rect, 270-self.rot)
			self.screen.blit(rot_sprite[0], (self.pos_on_screen[0], self.pos_on_screen[1]))

	def move(self, player_pos, camera_pos):
		if self.step_count >= self.num_steps:
			# We finally reached the player, prepare for the battle
			self.pos_on_screen = [player_pos[0], player_pos[1]]
			self.draw_me = True
			self.pos_on_map = [player_pos[0] + camera_pos[0], player_pos[1]+camera_pos[1]]
		else:
			# Converting player position on the camera to the position on the map
			player_pos_on_map = [camera_pos[0] + player_pos[0], camera_pos[1] + player_pos[1]]
			distance = [player_pos_on_map[0] - self.pos_on_map[0], player_pos_on_map[1] - self.pos_on_map[1]]

			on_screen = [False, False]

			for i in range(0,2):
				self.pos_on_map[i] += distance[i]/(self.num_steps - self.step_count)
				self.pos_on_screen[i] = self.pos_on_map[i] - camera_pos[i]
				if self.pos_on_screen[i] >= 0 and self.pos_on_screen[i] < self.camera_size[i]:
					on_screen[i] = True

			if on_screen[0] == True and on_screen[1] == True:
				self.draw_me = True

				# Plane rotation
				run = player_pos_on_map[0]-self.pos_on_map[0]
				rise = player_pos_on_map[1]-self.pos_on_map[1]
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

			self.step_count +=1

	def run(self, player_pos, camera_pos):
		self.move(plane_pos, camera_pos)
		self.draw()

	def upgrade(self):
		if self.era < 3:
			self.era += 1

	def collision(self, target):
		target_pos_on_screen = target
		if self.pos_on_screen[0] <= target_pos_on_screen[0] + 60 and self.pos_on_screen[0] >= target_pos_on_screen[0]:
			if self.pos_on_screen[1] <= target_pos_on_screen[1] + 60 and self.pos_on_screen[1] >= target_pos_on_screen[1]:
				print("collision")
				return True

# class battle_opponent:
# 	def __init__()
