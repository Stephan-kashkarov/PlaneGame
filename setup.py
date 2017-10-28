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

