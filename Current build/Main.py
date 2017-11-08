import pygame as pg
from Sprites import *
from settings import *
from sys import *
from functions import *

class game():
	"""docstring for screen"""
	def __init__(self, display_height, display_width, fps):
		pg.init()
		pg.mixer.init()
		self.camera_size = [display_width, display_height]
		self.fps = fps
		self.screen = pg.display.set_mode((self.camera_size[0], self.camera_size[1]))
		pg.display.set_caption(title)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(100, 50)
		self.era = 0
		self.load_data()
		self.camera_pos = [0,0]


	def button(self, msg, x, y, width, height, colour1, colour2, func = False): # button function
		mouse_pos = pg.mouse.get_pos() # Get the mouse position
		mouse_click = pg.mouse.get_pressed() # Get the mouse button state
		#print(mouse_pos)
		pg.draw.rect(self.screen, colour1, (x,y,width,height)) # render button
		if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y: # check if mouse is over button
			pg.draw.rect(self.screen, colour2, (x,y,width,height)) # change button colour
			if mouse_click[0] == 1 and func != None:
				func() # runs fuction
		else:
			pg.draw.rect(self.screen, colour1, (x,y,width,height)) # resting colour of button
		smallText = pg.font.Font("freesansbold.ttf", 40) # creates a font
		text_surf,text_rect = text_object(msg, smallText, black) #renders that font
		text_rect.center = ( (x+(width/2)), (y+(height/2)) ) # positions that font
		self.screen.blit(text_surf, text_rect) # print button


	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					pg.quit()
					quit()

	def load_data(self):
		self.biplane = pg.image.load("img/PLANE 2 N.png")
		self.monoplane = pg.image.load("img/PLANE 1 N.png")
		self.jetplane = pg.image.load("img/yak.png")
		self.player_img = pg.image.load("img/TPDWN.png")
		self.plane_img = pg.image.load("img/Player.png")
		self.alt_plane_img = pg.image.load("img/player_alt.png")
		self.full_logo = pg.image.load("img/full_logo.png")
		self.logo = pg.image.load("img/logo.png")
		self.trees = pg.image.load("img/treebttl.png")
		self.river = pg.image.load("img/riverbttl.png")
		self.grass = pg.image.load("img/grassbttl.png")
		self.quitscrn = pg.image.load("img/quit.png")
		self.map_group = [self.biplane, self.monoplane, self.jetplane]

		#map load
		self.map_img = pg.image.load("img/Eastern_front.png")
		self.map_rect = self.map_img.get_rect()
		self.map_width = self.map_img.get_width()
		self.map_height = self.map_img.get_height()
		self.map_size = [self.map_img.get_width(), self.map_img.get_height()]
		self.camera_pos = [0,0]
		#self.camera = Camera(self.map_width, self.map_height)

		#sprite load
		self.plane = battle_plane(self.screen, display_width/2, display_height/2, self.player_img)
		self.player = map_plane(200, 200, self.map_group, self.era, self.screen, self.camera_pos)


	def intro(self):
		self.screen.blit(self.full_logo, (0,0))
		intro = True
		while intro:
			self.events()
			click = pg.mouse.get_pressed() # Get the mouse button state
			if click[0] == 1:
				intro = False
			pg.display.flip()
			self.clock.tick(fps)

	def menu(self):
		self.screen.fill(black)
		pg.display.update()
		self.screen.blit(self.logo,(display_width/2-256/2, display_height/2-144/2))
		menu = True
		while menu:
			self.events()
			self.button("PLAY!", 200, 450, 200, 100, d_green, green, self.hq) # makes a play button
			self.button("QUIT!", 880, 450, 200, 100, d_red, red, quits) # makes a quit button

			pg.display.update()
			self.clock.tick(fps)

	def hq(self):
		self.screen.fill(grey)
		pg.draw.rect(self.screen, d_grey, (0, 0, 1280, 50))
		pg.draw.rect(self.screen, d_grey, (0, 500, 800, 220))
		roted_img = rot_center(self.jetplane, self.jetplane.get_rect(), 270)
		pg.draw.rect(self.screen, white, (0, 100, 1280, 150))
		self.screen.blit(roted_img[0], (200,100))
		self.screen.blit(self.jetplane, (50, 275))
		self.screen.blit(self.jetplane, (175, 275))
		self.screen.blit(self.jetplane, (300, 275))
		self.screen.blit(self.jetplane, (425, 275))
		buttons = True
		while buttons:
			self.button("Back!", 30, 530, 200, 180, red, d_red, self.menu)
			self.button("GO!", 490, 530, 200, 180, green, d_green, self.patrol)
			self.events()
			pg.display.flip()
			self.clock.tick(fps)


	def patrol(self):
		patroling = True
		self.screen.fill(black)

		self.camera_pos = [0,0]
		self.player.pos = [display_width/2, display_height/2]
		prev_player_pos = [display_width/2, display_height/2]

		offset_this_frame = [0,0]

		while patroling:
			self.player.move()
			# print("current_pos: ", self.player.pos, ", prev_player_pos: ", prev_player_pos)

			for i in range(0,2):
				offset_this_frame[i] = self.player.pos[i] - prev_player_pos[i]

				# Positive offset: moving towards the far edge of the map
				if offset_this_frame[i] >= 0:
					# print("positive")
					# Corner case: The camera is on the near side of the map and the player
					# is closer to the edge than the midscreen point
					if self.camera_pos[i] == 0 and prev_player_pos[i] < self.camera_size[i]/2:
						# print('1')
						# We move the plane rather then the camera
						if prev_player_pos[i] + offset_this_frame[i] > self.camera_size[i]/2:
							new_camera_offset = self.player.pos[i] - self.camera_size[i]/2
							self.player.pos[i] = self.camera_size[i]/2
							self.camera_pos[i] = new_camera_offset
							# print('2: ', "player_pos: ", self.player.pos[i], ", camera_pos: ", self.camera_pos[i], ", offset: ", offset_this_frame[i])
						# else:
						#     print('2_1: ', "player_pos: ", self.player.pos[i], ", camera_pos: ", self.camera_pos[i], ", offset: ", offset_this_frame[i])
						#   # We still have not reached midscreen point, we use the player position
						#   # calculated by the player.move() function
						#   pass
					# Another corner case: the camera is on the far side of the map,
					# we move the player until it reaches the far side of the screen
					elif self.camera_pos[i] + self.camera_size[i] >= self.map_size[i]:
						# print('3')
						if self.player.pos[i] >= self.camera_size[i]:
							self.player.pos[i] = self.camera_size[i]
							# print('4: ', "player_pos: ", self.player.pos[i], ", camera_pos: ", self.camera_pos[i], ", offset: ", offset_this_frame[i])
						# else:
						#     print('4_1: ', "player_pos: ", self.player.pos[i], ", camera_pos: ", self.camera_pos[i], ", offset: ", offset_this_frame[i])
						#   # We still have not reached the end of the screen, we use the player position
						#   # calculated by the player.move() function
						#   pass
					else:
						# This is the most common case: The camera is away from the edge of the map,
						# we move the camera while the player remains in the middle of the screen
						if self.camera_pos[i] + self.camera_size[i] + offset_this_frame[i] < self.map_size[i]:
							self.player.pos[i] = self.camera_size[i]/2
							self.camera_pos[i] += offset_this_frame[i]
							# print('5: ', "player_pos: ", self.player.pos[i], ", camera_pos: ", self.camera_pos[i], ", offset: ", offset_this_frame[i])
						else:
							# Here we move the camera to the far edge of the screen, and then start moving the player
							new_player_offset = self.map_size[i] - (self.camera_pos[i] + self.camera_size[i])
							self.camera_pos[i] = self.map_size[i] - self.camera_size[i]
							self.player.pos[i] = self.camera_size[i]/2 + new_player_offset
							# print('6: ', "player_pos: ", self.player.pos[i], ", camera_pos: ", self.camera_pos[i], ", offset: ", offset_this_frame[i])
				# # Negative offset, moving towards the near edge of the map
				# else:
				#   # Corner case: the camera is on the far edge of the map, and the player between the
				#   # far edge of the screen and the midscreen point
				#   if self.camera_pos[i] + self.camera_size[i] == self.map_size[i]:
				#       # we move the player
				#       pass

				prev_player_pos[i] = self.player.pos[i]

			# print("prev_player_pos: ", prev_player_pos)

			self.screen.blit(self.map_img, (-self.camera_pos[0], -self.camera_pos[1]))
			self.player.run()
			self.events()
			pg.display.update()
			# collision = self.player.col()
			# if collision != False:
			#   if collision == tank:
			#       self.battle(tank)



	def battle(self, scene):
		self.screen.fill(black)
		battle = True
		while battle:
			self.screen.blit(scene, (0,0))
			self.events()
			self.plane.run()
			pg.display.update()

	def test(self):
		plane = battle_plane(self.screen, display_width/2, display_height/2, self.player_img)
		self.screen.fill(black)
		test = True
		while test:
			self.screen.fill(black)
			self.events()
			plane.run()
			pg.display.flip()
			self.clock.tick()

	def upgrade(self):
		# plane.upgrade()
		# player.upgrade()
		pass

	def quitscreen(self):
		end = True
		while end:
			self.screen.blit(self.quitscrn, (0,0))
			self.button("QUIT!", display_width/2, display_height/2, 200, 100, d_red, red, quits) # makes a quit button
			pg.display.update()


instance = game(display_height, display_width, fps)
# instance.intro()
# instance.menu()
instance.quitscreen()
#instance.patrol()
#instance.battle(instance.river)
#instance.test()
#while instance:
#   instance.hq()
#   instance.patrol()
#       instance.battle()
#instancee.boss()
#quit()
