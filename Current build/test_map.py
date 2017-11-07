from game_map import *
import pygame as pg
from settings import *


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

	def load_data(self):

		self.map = TiledMap("img/Eastern_Front.tmx")
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
		self.camera = Camera(self.map.width, self.map.height)

	def prints(self):
		while True:
			self.screen.blit(self.map_img, (0,0))
			print(self.map_rect)
			pg.draw.rect(self.screen, red, (1030, 530, 230, 180))
			pg.display.update()


Game = game(display_height, display_width, fps)
Game.prints()
