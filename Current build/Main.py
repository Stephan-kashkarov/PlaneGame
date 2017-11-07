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
		self.height = display_height
		self.width = display_width
		self.fps = fps
		self.screen = pg.display.set_mode((self.width, self.height))
		pg.display.set_caption(title)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(100, 50)
		self.era = 0
		self.load_data()
		self.camera = [0,0]


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
		self.map_group = [self.biplane, self.monoplane, self.jetplane]

		#map load
		self.map_img = pg.image.load("img/Eastern_front.png")
		self.map_rect = self.map_img.get_rect()
		self.map_width = self.map_img.get_width()
		self.map_height = self.map_img.get_height()
		self.camera = [0,0]
		#self.camera = Camera(self.map_width, self.map_height)

		#sprite load
		self.plane = battle_plane(self.screen, display_width/1*4, display_height/1*4, self.player_img)
		self.player = map_plane(200, 200, self.map_group, self.era, self.screen, self.camera)
		self.enemy = opponent(self.screen, display_width/3*4, display_height/3*4, self.player_img)

	def tutorial(self):
		pass

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
		self.screen.blit(self.logo,(display_width/2, display_height/2))
		menu = True
		while menu:
			self.events()
			self.button("PLAY!", 200, 450, 200, 100, d_green, green, self.hq) # makes a play button
			self.button("TUTORIAL!", 540, 450, 200, 100, d_grey, grey, self.tutorial) # makes a manual button
			self.button("QUIT!", 880, 450, 200, 100, d_red, red, quits) # makes a quit button

			pg.display.update()
			self.clock.tick(fps)

	def hq(self):
		self.screen.fill(black)
		pg.draw.rect(self.screen, d_grey, (0, 0, 1280, 50))
		pg.draw.rect(self.screen, d_grey, (0, 500, 800, 220))
		pg.draw.rect(self.screen, d_grey, (1000, 500, 280, 220))
		pg.draw.rect(self.screen, black, (1030, 530, 230, 180))
		buttons = True
		while buttons:
			self.button("Back!", 30, 530, 200, 180, red, d_red, self.menu)
			self.button("Upgrade!", 260, 530, 200, 180, grey, dd_grey, self.upgrade)
			self.button("GO!", 490, 530, 200, 180, green, d_green, self.patrol)
			self.events()
			pg.display.flip()
			self.clock.tick(fps)


	def patrol(self):
		self.camera = [0,0]

		patroling = True
		self.screen.fill(black)
		while patroling:
			if self.player.pos[0] >= self.map_width + display_width/2:
				self.camera[0] = self.map_width + display_width/2
			else:
				self.camera_x = self.player.pos[0] - display_width/3
				self.camera[0] = self.camera_x
				self.playerx = self.player.pos[0]

			if self.player.pos[1] >= self.map_height + display_height/2:
				self.camera[0] = self.map_height + display_height/2
			else:
				self.camera_y = self.player.pos[1] - display_height/3
				self.camera[1] = self.camera_y
				self.playery = self.player.pos[1]

			self.screen.blit(self.map_img, (0 - self.camera[0], 0 - self.camera[1]))
			self.player.run()
			self.events()
			pg.display.update()
			# collision = self.player.col()
			# if collision != False:
			# 	if collision == tank:
			# 		self.battle(tank)



	def battle(self):
		self.screen.fill(black)
		battle = True
		while battle:
			screen.blit(battle_backgroud.png, (0,0))
			self.player.run()
			self.enemy.run()

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


instance = game(display_height, display_width, fps)
# instance.intro()
# instance.menu()
instance.patrol()
#instance.test()
#while instance:
#	instance.hq()
#	instance.patrol()
#		instance.battle()
#instance.boss()
#quit()
