#IMPORTS
import pygame
import time
import random
import math
import sys
import engine.py


# INITIALIZATION
pygame.init()

#GAME VARIABLES
display_width = 1280 # Width of the pygame display
display_height = 720 # height of the pygame dispaly
fps = 120 # Frames per second
kills = 0 # number of kills
xp = 0 # Experience points

#PHYSICS VARIABLES
gravity = 9800 # Gravity Coeficient
drag_coef = 1 # Drag coeficient
thrust_coef = 65536 # thrust coeficient


#COLOURS
black = (0,0,0) # the Black colour in RBG
grey = (100,100,100) # the Grey colour in RBG
d_grey = (50,50,50) # the Dark Grey colour in RBG
white = (255,255,255) # the White colour in RBG
red = (255,0,0) # the Red colour in RBG
d_red = (200,0,0) # the Dark Red colour in RBG
green = (0,255,0) # the Green colour in RBG
d_green = (0,200,0) # the Dark green colour in RBG
blue = (0,0,255) # the Blue colour in RBG

#DISPLAY INIT
display_resolution = (display_width,display_height) # Overall resolution of display
gameDisplay = pygame.display.set_mode(display_resolution) # makes the disp;ay windown
pygame.display.set_caption("Plane tech demo") # sets a name for the display window
clock = pygame.time.Clock() # Fps Speed

#SPRITE DEF
player_sprite = pygame.image.load("Planes/Player.png") # makes the player sprite
player_sprite_alt = pygame.image.load("Planes/Player_alt.png") # an upsided down player sprite
background = pygame.image.load("Planes/Background 1.png") # makes the background
sprite_width = 10 # Width of sprite in pxls
sprite_height = 12 # hight of the sprite in pxls

def player(x, y): # prints the player
	gameDisplay.blit(player_img, (x, y)) # prints the player sprite at x,y

def sprite(sprite, x, y): # printst other objects
	gameDisplay.blit(sprite, (x, y)) # prints a sprite at x,y

def leave(): # Quit function
	pygame.quit() # pygame de initialize
	quit() # quit python

def text_object(text, font, colour): # text fuction
	text_surface = font.render(text, True, colour) #renders font
	return text_surface, text_surface.get_rect() # returns the text object

def button(msg, x, y, width, height, colour1, colour2, func = False): # button function
	mouse_pos = pygame.mouse.get_pos() # Get the mouse position
	mouse_click = pygame.mouse.get_pressed() # Get the mouse button state
	#print(mouse_pos)
	pygame.draw.rect(gameDisplay, colour1, (x,y,width,height)) # render button
	if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y: # check if mouse is over button
		pygame.draw.rect(gameDisplay, colour2, (x,y,width,height)) # change button colour
		if mouse_click[0] == 1 and func != None:
			func() # runs fuction

	else:
		pygame.draw.rect(gameDisplay, colour1, (x,y,width,height)) # resting colour of button
	smallText = pygame.font.Font("freesansbold.ttf", 40) # creates a font
	text_surf,text_rect = text_object(msg, smallText, black) #renders that font
	text_rect.center = ( (x+(width/2)), (y+(height/2)) ) # positions that font
	gameDisplay.blit(text_surf, text_rect) # print button

#def score(num): # score display function
#	gameDisplay.fill(black)
#	message_display("you killed, " + str(num),display_width/2,display_height/2, white)
#	game()

def rot_center(image, rect, angle): # came from stack overflow
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

	def shoot(): # shoot function
		pass

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

		button("PLAY!", 200, 450, 200, 100, d_green, green, main) # makes a play button
		button("Planes", 540, 450, 200, 100, d_grey, grey,planes) # makes a manual button
		button("QUIT!", 880, 450, 200, 100, d_red, red, leave) # makes a quit button

		pygame.display.update()
		clock.tick(fps)

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

def travel():

	game_end = False
	while not game_end: # game loop
		for event in pygame.event.get(): # check for input
			if event.type == pygame.QUIT: # quit funct
					pygame.quit()
					quit()
			if event.type == pygame.KEYDOWN: #if a key is pressed
				if event.key == pygame.K_UP: # if that key is up
					x_change = 2
				elif event.key == pygame.K_DOWN: # if key is down
					x_change = -2
				if event.key == pygame.K_LEFT: # left key
					y_change = 2
				elif event.key == pygame.K_RIGHT:# Right key
					y_change = -2
			elif event.type == pygame.KEYUP: # if key stops being pressed
				y_change = 0 # set change to 0
				x_change = 0 # set change to 0

		player.x += x_change # and the change to value
		player.y += y_change # add the change to value


def main(): #main function of code
	kills = 0 # score keeper
	player = plane(player_sprite, 0, 720, 0, True) # make a object in class plane
	attack_angle_change = 0 # set a variable to add to attack angel near the end of loop
	game_end = False # Exit variable
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

			elif event.type == pygame.KEYUP: # if key stops being pressed
				attack_angle_change = 0 # set change to 0
				speed_change = 0 # set change to 0

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

		text_surf, text_rect = text_object("Speed: " + str(((round(math.sqrt(player.velocity_x**2 + player.velocity_y**2)))*18)/5) + "km/h", large_text, black) # makes a speedometer
		text_rect.center = ((40), (40)) # positions text
		gameDisplay.blit(text_surf,text_rect) # prints text


		player.move() # simulates one frame of movemnt
		if player.y <= 0: # checks if sprite is too low
			player.y = 0  # sets a floor
		player.draw() # draws the plane

		#DISPLAY UPDATE
		pygame.display.update() # updates the display
		clock.tick(fps) # sets fps

intro() # runs intro
planes() # runs maual
battle() # runs battle

pygame.quit() # quits pygame
quit() # exit
