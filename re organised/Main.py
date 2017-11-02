#main
import pygame as pg
import random
from temp_settings import *

class Game:
	def __init__(self):
		#initializer
		pg.init()
		pg.mixer.init()
		self.running = True
		self.screen = pg.display.set_mode((width,height))
		pg.set_caption(title)
		self.clock = pg.time.Clock()


	def game_init(self):
		#initiaizes game
		self.all_sprites = pg.sprites.Group()
		self.playing = True
		self.run()

	def run(self):
		#game loop
		self.playing = True
		while self.playing:
			self.clock.tick(fps)
			self.events()
			self.draw()

	def update(self):
		#game loop update
		self.all_sprites()

	def events(self):
		#game loop events
		mouse_pos = pg.mouse.get_pos() # Get the mouse position
		mouse_click = pg.mouse.get_pressed() # Get the mouse button state
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						pygame.quit()
						quit()
				if event.type == pygame.KEYDOWN:
					pass
				elif event.type == pygame.KEYUP:
					pass

	def draw(self):
		#game loop draw
		self.screen.fill(black)
		self.all_sprites.draw(sreen)
		pg.display.flip()


	def start(self):
		pass

	def end(self):
		pass

g = Game()
g.start()
while g.running:
	g.new()
	g.end()
pygmae.quit()
quit()
