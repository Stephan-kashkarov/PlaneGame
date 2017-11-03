import pygame as pg
from sprites import *
from settings import *
from game_map import *

class game():
	"""docstring for screen"""
	def __init__(self, display_height, display_width, fps):
		pg.init()
		pg.mixer.init()
		self.display_height = display_height
		self.display_width = display_width
		self.fps = fps
		self.screen = pg.display.set_mode((width,height))
		pg.display.set_caption(title)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(100, 50)
		self.load_data()

	def load_data(self):
		pass

	def intro(self):
		pass

	def menu(self):
		pass

	def hq(self):
		pass

	def patrol(self):
		pass

	def battle(self):
		pass





#game.intro()
#game.menu()
#while game:
#	game.hq()
#	game.patrol()
#		game.battle()
#game.boss()
#quit()
