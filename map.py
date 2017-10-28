import pygame
import time
import random
import math
import sys
from setup import *
from functions import *
import pytmx

class main_map():
	def __init__(self, filename):
		mp = pytmx.load_pygame(filename, pixelalpha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm

	def render(self,surface):
		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_Layers:
			if isinstance(layer,pytmx.TiledTileLayer):
				for x, y, gid, in layer:
					tile = ti(gid)
					if tile:
						gameDisplay.blit(tile, x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight)
	def make_map(self):
		temp_surf = pygame.gameDisplay((self.height, self.width))
		self.render(temp_surf)
		return temp_surf
