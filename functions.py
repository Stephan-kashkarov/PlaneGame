#defines

import pygame
import time
import random
import math

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

def collision(x, y, playerx, playery, width, height, playerwidth, playerheight):
	for obj in range(x,width):
		for itm in range(y, height):
			if obj in range(playerx,playerwidth) and if itm in range(playery, playerheight):
				return True
	else:
		return False
