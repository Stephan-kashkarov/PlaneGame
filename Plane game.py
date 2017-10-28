#IMPORTS
import pygame
import time
import random
import math
import sys
from engine import *
from setup import *
from functions import *

#var
kills = 0 # number of kills
xp = 0 # Experience points

class man():
	def __init__ (self, sprite, x, y, rotation):
		self.sprite = sprite
		self.rect = sprite.get_rect()
		self.x = x
		self.y = y
		self.rotation = rotation
		self.rect = sprite.get_rect()

	def move(self):
	# Directional movement
		self.x += math.cos(math.radians(self.rotation))*10
		self.y += math.sin(math.radians(self.rotation))*10



	def draw(self):
		img, img_rect = rot_center(self.sprite, self.rect, self.rotation*-1)
		gameDisplay.blit(img, (self.x,self.y))

player = man(playerhome, 0, 0, 0)

def intro(): # The intro to the game include the main menu

	intro = True

	while intro: # intro loop
		for event in pygame.event.get(): # quit check
			if event.type == pygame.QUIT:
					pygame.quit()
					quit()

		gameDisplay.fill(black) # make background black
		large_text = pygame.font.Font("freesansbold.ttf",115)
		text_surf, text_rect = text_object("Mother Land", large_text, white)
		text_rect.center = ((display_width/2), (display_height/2))
		gameDisplay.blit(text_surf,text_rect)

		button("PLAY!", 200, 450, 200, 100, d_green, green, menu) # makes a play button
		button("TUTORIAL!", 540, 450, 200, 100, d_grey, grey,tutorial) # makes a manual button
		button("QUIT!", 880, 450, 200, 100, d_red, red, leave) # makes a quit button

		pygame.display.update()
		clock.tick(fps)

def tutorial():
	pass

def menu():
	game_end = False
	speed_change = 0
	mve = False
	rotation_change = 0
	while not game_end:

		# EVENT LOOP
		mouse_pos = pygame.mouse.get_pos() # Get the mouse position
		mouse_click = pygame.mouse.get_pressed() # Get the mouse button state
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
						mve = True
				elif event.key == pygame.K_DOWN:
						mve = True

			elif event.type == pygame.KEYUP:
				rotation_change = 0
				mve = False
		run = mouse_pos[1]-player.y
		rise = mouse_pos[0]-player.x
		if rise == 0:
			rise = 1
		gradiant = (run)/(rise)

		print(gradiant)
		player.rotation = math.degrees(math.atan(gradiant))
		gameDisplay.blit(intromap,(0,0))
		if mve == True:
			player.move()
			#x1, y1, x2, y2, playerx1, playery1, playerx2, playery2
			settings = collision(76, 241, 339, 333, player.x, player.y, player.x + 63, player.y + 89)
			briefing = collision(81, 364, 341, 456, player.x, player.y, player.x + 63, player.y + 89)
			helps = collision(81, 480, 343, 570, player.x, player.y, player.x + 63, player.y + 89)
			planes = collision(704, 253, 1019, 592, player.x, player.y, player.x + 63, player.y + 89)
			if settings == True:
				settings()
			if briefing == True:
				briefing()
			if helps == True:
				helps()
			if planes == True:
				planes()
		player.draw()

		#DISPLAY UPDATE
		pygame.display.update() # updates the display
		clock.tick(fps) # sets fps


def planes(): # manual screen
	planes = True
	while planes:
		for event in pygame.event.get(): # quit function
			if event.type == pygame.QUIT:
					pygame.quit()
					quit()

		gameDisplay.fill(d_grey)
		large_text = pygame.font.Font("freesansbold.ttf",57)
		text_surf, text_rect = text_object(" Manual ", large_text, white)
		text_rect.center = ((display_width/2), (display_height/9.5))
		gameDisplay.blit(text_surf,text_rect)
		pygame.draw.rect(gameDisplay, grey, (30, 100, 550, 600))
		pygame.draw.rect(gameDisplay, grey, (display_width - 600 , 100, 550, 600))


		pygame.display.update()
		clock.tick(fps)

def battle():
	player = plane(player_sprite, 0, 720, 0, True) # make a object in class plane
	attack_angle_change = 0 # set a variable to add to attack angel near the end of loop
	game_end = False # Exit variable
	play = False # testing var
	speed_change = 0 # set a variable to add to throttle near the end of loop
	while not game_end: # game loop
		for event in pygame.event.get(): # check for input
			if event.type == pygame.QUIT: # quit funct
					pygame.quit()
					quit()
			if event.type == pygame.KEYDOWN: #if a key is pressed
				if event.key == pygame.K_UP: # if that key is up
					if player.throttle <= 0.9: # if the throttle is not max
						speed_change = 0.1 # set speed to 10%
				elif event.key == pygame.K_DOWN: # if key is down
					if player.throttle >= 0.1: #check throttle is not min
						speed_change = -0.1 # set the throttle to -10%
				if event.key == pygame.K_LEFT: # left key
					attack_angle_change = -5 # set delta angle to -5
					if attack_angle_change >= 360: # allows for sub 360* movemnt
						attack_angle_change -= 360
				elif event.key == pygame.K_RIGHT:# Right key
					attack_angle_change = 5 # sets delta ange to +5
					if attack_angle_change >= 360: #allows for sub 360* movement
						attack_angle_change -= 360

				elif event.key == pygame.K_SPACE:
					play = True # testing var

			elif event.type == pygame.KEYUP: # if key stops being pressed
				attack_angle_change = 0 # set change to 0
				speed_change = 0 # set change to 0
				play = False # testing var


		player.attack_angle += attack_angle_change # and the change to value
		player.throttle += speed_change # add the change to value

		if player.attack_angle <= 90 or player.attack_angle >=270: # makes the sprite alwas face upwards
			player.sprite = player_sprite # sprite 1
		else:
			player.sprite = player_sprite_alt # sprite 2


		#debug circuit (could be used for crash detection)
		if player.x + sprite_width >= display_width: #left border
			player.x = display_width/2
			player.y = display_height - sprite_height - 5
		elif player.x <= 0: #right border
			player.x = display_width/2
			player.y = display_height - sprite_height - 5
		elif player.y <= 0: #top border
			player.x = display_width/2
			player.y = display_height - sprite_height - 5
		elif player.y + sprite_height >= display_height: #bottom border
			player.x = display_width/2
			player.y = display_height - sprite_height - 5

		# DRAW LOOP
		gameDisplay.blit(background, (0,0)) # prints the background

		large_text = pygame.font.Font("freesansbold.ttf", 10) # renders font
		text_surf, text_rect = text_object("Trottle: " + str(round(100*player.throttle)) + "%", large_text, black) # makes a throttle counter
		text_rect.center = ((40), (20)) # positions the text
		gameDisplay.blit(text_surf,text_rect) # prints text

		text_surf, text_rect = text_object("Speed: " + str(round((player.velocity*18)/5)) + "km/h", large_text, black) # makes a speedometer
		text_rect.center = ((40), (40)) # positions text
		gameDisplay.blit(text_surf,text_rect) # prints text

		if play == True: #testing var
			player.move() # simulates one frame of movemnt
		if player.y <= 0: # checks if sprite is too low
			player.y = 0  # sets a floor
		player.draw() # draws the plane

		#DISPLAY UPDATE
		pygame.display.update() # updates the display
		clock.tick(fps) # sets fps

intro() # runs intro
#planes() # runs maual
#battle() # runs battle
menu()
pygame.quit() # quits pygame
quit() # exit
