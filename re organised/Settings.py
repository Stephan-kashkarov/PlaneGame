import pygame as pg

#PLAYER STATS
PLAYER_SPEED = 100

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

#SCREEN STATS
display_width = 1280
display_height = 720
fps = 120
title = "plane_game"


def text_object(text, font, colour): # text fuction
	text_surface = font.render(text, True, colour) #renders font
	return text_surface, text_surface.get_rect() # returns the text object

def rot_center(image, rect, angle): # came from stack overflow
    """rotate an image while keeping its center"""
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

def quits():
	pg.quit()
	quit()
