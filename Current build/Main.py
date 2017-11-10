import pygame as pg
from Sprites import *
from settings import *
from sys import *
from functions import *

class game():
	"""Class of the game"""
	def __init__(self, display_height, display_width, fps):
		pg.init() # initializes pygame
		pg.mixer.init()
		self.camera_size = [display_width, display_height] #sets the dimetions for screen
		self.fps = fps # setst the fps
		self.screen = pg.display.set_mode((self.camera_size[0], self.camera_size[1])) # makes the sreen
		pg.display.set_caption(title) # makes the title
		self.clock = pg.time.Clock()
		pg.key.set_repeat(100, 50) # allows key repeat
		self.loadingscrn = pg.image.load("img/loadingscrn.png")
		self.screen.blit(self.loadingscrn, (0,0))
		pg.display.update()
		self.era = 0
		self.load_data() # loads all the data for game
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


	def events(self): # quit button loop
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					pg.quit()
					quit()

	def load_data(self): # loads all sprites
		self.biplane = pg.image.load("img/PLANE 2 N.png")
		self.monoplane = pg.image.load("img/PLANE 1 N.png")
		self.jetplane = pg.image.load("img/yak.png")
		# self.tonk_sprite = pg.image.load("img/tonk.png")
		self.plane_img = pg.image.load("img/Player.png")
		self.alt_plane_img = pg.image.load("img/player_alt.png")
		self.full_logo = pg.image.load("img/full_logo.png")
		self.logo = pg.image.load("img/logo.png")
		self.trees = pg.image.load("img/treebttl.png")
		self.river = pg.image.load("img/riverbttl.png")
		self.grass = pg.image.load("img/grassbttl.png")
		self.quitscrn = pg.image.load("img/quit.png")
		self.loadingscrn = pg.image.load("img/loadingscrn.png")
		self.bull_sprite = pg.image.load("img/bullet.png")
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
		self.plane = battle_plane(self.screen, display_width/2, display_height/2, self.jetplane, self.bull_sprite)
		self.enemy = battle_opponent(self.screen, self.jetplane, self.bull_sprite)
		self.player = map_plane(200, 200, self.map_group, self.era, self.screen)

		self.opponents = []

		for i in range(5):
			self.opponents.append(map_opponent(self.map_group, self.era, self.screen, self.camera_size, self.map_size))

		#music load
		self.intromusic = pg.mixer.music.load("music/SOV_anthem.mp3")
		# self.shoot = pg.mixer
		self.endmusic = pg.mixer.music.load("music/game_music.mp3")

	def intro(self): # intro screen
		self.screen.blit(self.full_logo, (0,0)) # logo print
		intro = True
		while intro:
			self.events()
			click = pg.mouse.get_pressed() # Get the mouse button state
			if click[0] == 1: #checks for clicks
				intro = False
			pg.display.flip()
			self.clock.tick(fps)

	def menu(self):# meny screen
		self.screen.fill(black) # makes black background
		pg.display.update()
		self.screen.blit(self.logo,(display_width/2-256/2, display_height/2-144/2))
		menu = True
		while menu: #menu loop
			self.events()
			self.button("PLAY!", 200, 450, 200, 100, d_green, green, self.hq) # makes a play button
			self.button("QUIT!", 880, 450, 200, 100, d_red, red, quits) # makes a quit button

			pg.display.update()
			self.clock.tick(fps)

	def hq(self): # sub menu screen
		self.screen.fill(grey) # draw gui
		pg.draw.rect(self.screen, d_grey, (0, 0, 1280, 50)) # draw gui
		pg.draw.rect(self.screen, d_grey, (0, 500, 800, 220)) # draw gui
		roted_img = rot_center(self.jetplane, self.jetplane.get_rect(), 270) # draw gui
		pg.draw.rect(self.screen, white, (0, 100, 1280, 150)) # draw gui
		self.screen.blit(roted_img[0], (200,100)) # draw gui
		self.screen.blit(self.jetplane, (50, 275)) # draw gui
		self.screen.blit(self.jetplane, (175, 275)) # draw gui
		self.screen.blit(self.jetplane, (300, 275)) # draw gui
		self.screen.blit(self.jetplane, (425, 275)) # draw gui
		buttons = True
		while buttons: #buttons
			self.button("Back!", 30, 530, 200, 180, red, d_red, self.menu)
			self.button("GO!", 490, 530, 200, 180, green, d_green, self.patrol)
			self.events()
			pg.display.flip()
			self.clock.tick(fps)


	def patrol(self): #Patrol phase
		patroling = True
		self.screen.fill(black)
		self.camera_pos = [0,0]
		self.player.pos = [display_width/2, display_height/2]
		prev_player_pos = [display_width/2, display_height/2]

		offset_this_frame = [0,0]

		while patroling: # patrol loop
			self.player.move() # simulates plane for one step
			# print("current_pos: ", self.player.pos, ", prev_player_pos: ", prev_player_pos)

			for i in range(0,2):
				offset_this_frame[i] = self.player.pos[i] - prev_player_pos[i]

				# Positive offset: moving towards the far edge of the map
				if offset_this_frame[i] >= 0:
					# print("positive")
					# Corner case: The camera is on the near side of the map and the player
					# is clo1ser to the edge than the midscreen point
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
				# Negative offset, moving towards the near edge of the map
				else:
					# Corner case: the camera is on the far edge of the map, and the player between the
					# far edge of the screen and the midscreen point
					if self.camera_pos[i] + self.camera_size[i] == self.map_size[i]:
						if self.player.pos[i] < self.camera_size[i]/2:
							# the player reached the screen midpoint, start moving the camera
							new_camera_offset =  self.camera_size[i]/2 - self.player.pos[i]
							self.player.pos[i] = self.camera_size[i]/2
							self.camera_pos[i] -= new_camera_offset
						else:
							# we move the player
							pass
					# Corner case: the camera is on the near edge of the map, and the player between the
					# near edge of the screen and the midscreen point
					elif self.camera_pos[i] <= 0:
						self.camera_pos[i] = 0
						if self.player.pos[i] <= 0:
							self.player.pos[i] = 0
						else:
							# we move the player
							pass
					else:
						# This is the most common case: The camera is away from the map's edges, we move the camera keeping the played in the middle of the screen
						if self.camera_pos[i] + offset_this_frame[i] < 0:
							# The offset exceeds the distance between the camera pos and the near edge of the map, we move the camera pos to the edge of the map
							# and then start moving the player left from the midscreen point
							new_player_offset = self.camera_pos[i]
							self.camera_pos[i] = 0
							self.player.pos[i] -= new_player_offset
						else:
							self.player.pos[i] = self.camera_size[i]/2
							self.camera_pos[i] += offset_this_frame[i]  # here offset is negtive, as a result camera pos will move left

				prev_player_pos[i] = self.player.pos[i]

			for opponent in self.opponents: # move alive opponents
				if not opponent.defeated:
					opponent.move(self.player.pos, self.camera_pos)

			# print("prev_player_pos: ", prev_player_pos)
			col_check = self.player.collision(1227, 490, self.camera_pos) # airport collision check
			if col_check != True:
				col_check = self.player.collision(521, 5192, self.camera_pos)
				if col_check != True:
					col_check = self.player.collision(154, 1354, self.camera_pos)
					if col_check != True:
						col_check = self.player.collision(665, 3385, self.camera_pos)

			if col_check == True:
				self.hq()

			col_check = self.player.collision(1243, 3784, self.camera_pos)  # airport collision check
			if col_check != True:
				col_check = self.player.collision(2581, 49, self.camera_pos)
				if col_check != True:
					col_check = self.player.collision(3549, 6466, self.camera_pos)
					if col_check != True:
						col_check = self.player.collision(1541, 7834, self.camera_pos)

			if col_check == True:
				self.hq()

			if col_check != True:
				col_check = self.player.collision(6344, 6854, self.camera_pos)  # airport collision check
				if col_check != True:
					col_check = self.player.collision(6076, 4311, self.camera_pos)
					if col_check != True:
						col_check = self.player.collision(6632, 1605, self.camera_pos)

			if col_check == True:
				self.hq()

			for opponent in self.opponents: # checks for opponent collision
				if not opponent.defeated:
					battle_check = opponent.collision(self.player.pos)
					if battle_check == True:
						self.battle()

			self.screen.blit(self.map_img, (-self.camera_pos[0], -self.camera_pos[1])) #print camera with map
			self.player.draw()

			for opponent in self.opponents: # print alive opponents
				if not opponent.defeated:
					opponent.draw()

			self.events()
			pg.display.update()
			# collision = self.player.col()
			# if collision != False:
			#   if collision == tank:
			#       self.battle(tank)



	def battle(self): # battle sequence
		self.screen.fill(black)
		battle = True
		random_num = random.randint(0,2) # randomise map
		if random_num == 0:
			scene = self.trees
		if random_num == 1:
			scene = self.river
		if random_num == 2:
			scene = self.grass
		
		self.enemy.reset()

		while battle:
			self.screen.blit(scene, (0,0))
			self.events()
			self.plane.events() # checks for input
			win = self.plane.move(self.enemy.pos) #checks for crash into ground
			kill = self.enemy.move(self.plane.pos)
			self.plane.draw()
			self.enemy.draw()
			if kill == True:
				self.quitscreen()
			if win == True:
				self.patrol()

			pg.display.update()

	def upgrade(self):
		# plane.upgrade()
		# player.upgrade()
		pass

	def quitscreen(self): # death screen
		end = True
		while end:
			self.screen.blit(self.quitscrn, (0,0))
			self.button("QUIT!", display_width/2, display_height/2, 200, 100, d_red, red, quits) # makes a quit button
			pg.display.update()


instance = game(display_height, display_width, fps)
# instance.intro()
# instance.menu()
# instance.patrol()
instance.battle()
# # quit()
