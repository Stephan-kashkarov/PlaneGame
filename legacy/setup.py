#Setup
import pygame
import time
import random
import math
import pytmx

# INITIALIZATION
pygame.init()
#GAME VARIABLES
display_width = 1280 # Width of the pygame display
display_height = 720 # height of the pygame dispaly
fps = 120 # Frames per second

#PHYSICS VARIABLES
gravity = 9800 # Gravity Coeficient
drag_coef = 1 # Drag coeficient
thrust_coef = 65536 # thrust coeficient
lift_coef = 10

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
intromap = pygame.image.load("Planes/Airbase.png")
playerhome = pygame.image.load("Planes/TPDWN.png")

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


