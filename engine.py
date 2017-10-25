#engine.py

#IMPORTS
import pygame
import time
import random
import math
import sys
import functions
import setup

#GAME VARIABLES
display_width = 1280 # Width of the pygame display
display_height = 720 # height of the pygame dispaly
fps = 120 # Frames per second

#PHYSICS VARIABLES
gravity = 9800 # Gravity Coeficient
drag_coef = 1 # Drag coeficient
thrust_coef = 65536 # thrust coeficient

#PYGAME WINDOW SETUP
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

def rot_center(image, rect, angle): # came from stack overflow
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

class plane(): # class of plane
	def __init__ (self, sprite, x, y, attack_angle, ai):
		self.sprite = sprite # sprite file goes here
		self.rect = sprite.get_rect() # makes the rect to said sprite
		self.x = x # X pos
		self.y = y # y pos
		self.attack_angle = attack_angle # angle that the sprite is facing
		self.shoot = False # shoot check
		self.state = True # dead or alive
		self.ai = ai # check for AI
		self.throttle = 0.0 # throttle of sprite
		self.velocity_x = 0 # velocity in the x direction
		self.velocity_y = 0 # velocity in the y direction
		self.drag_force = 0 # drag variable
		self.lift_force = 0 # lift variable
		self.thrust = 0 # thrust variable
		self.mass = 1000 # mass of plane


	def move(self): # physics simulation
		# Var
		print("attack angle: ", self.attack_angle)
		# Thrust pushes the plane forward, depends on the position of the throttle
		self.thrust_x = thrust_coef * self.throttle * math.cos(math.radians(self.attack_angle))
		self.thrust_y = thrust_coef * self.throttle * math.sin(math.radians(self.attack_angle))
		print ("thrust_x: ", self.thrust_x, ", thrust_y: ", self.thrust_y)

		# Drag force is caused by air friction and acts in the direction opposite to thrust
		self.drag_force_x = drag_coef * (self.velocity ** 2) * math.cos(math.radians(self.attack_angle))
		self.drag_force_y = drag_coef * (self.velocity ** 2) * math.sin(math.radians(self.attack_angle))
		print ("drag_x: ", self.drag_force_x, ", drag_y: ", self.drag_force_y)

		# Lift force is created by wing geometry, acts in the direction perpendicular the the wing surface
		self.lift_force_y = gravity + lift_coef * (self.velocity ** 2) * math.sin(math.radians(2*self.attack_angle))
		self.lift_force_x = lift_coef * math.sin(math.radians(2*self.attack_angle))
		print ("lift_y: ", self.lift_force_y, ", lift_x: ", self.lift_force_x)

		total_force_x = self.thrust_x - self.drag_force_x - self.lift_force_x;
		total_force_y = self.lift_force_y + self.thrust_y - gravity - self.drag_force_y
		print ("total_force_x: ", total_force_x, ", total_force_y: ", total_force_y)


		# New velocity is based on the velocity on the previous frame and the force acting on the plane on the current frame.
		# F = ma = m(v1-v0)/t; v1 = v0 + Ft/m, where t = 1/fps, so v1 = v0 + F/(fps*m)
		self.velocity_x += total_force_x/(fps*self.mass)
		self.velocity_y = total_force_y/(fps*self.mass)

		self.velocity = math.sqrt(self.velocity_x**2 + self.velocity_y**2)

		print ("velocity_x: ", self.velocity_x, ", velocity_y: ", self.velocity_y)
		print ("total velocity: ", self.velocity)

		# Conversion from m/s to pixels/frame
		delta_x = 4 * self.velocity_x/fps
		delta_y = 4 * self.velocity_y/fps

		# Y force
		#t_y = self.throttle * math.sin(math.radians(self.attack_angle)) # Thrust calculation on the y plane
		#d_y = self.drag_force * math.sin(math.radians(self.attack_angle)) # drag calculation on the y plane
		#l_y = self.lift_force * math.cos(math.radians(self.attack_angle)) # lift calculation on the y plane
		#g_y = self.mass * gravity # gravity calculation on the y plane
		#f_y = t_y - d_y - g_y # Total force in y direction  + l_y
		#self.y += (f_y * 1/fps)/self.mass + self.y
		# X force
		#t_x = self.throttle * math.cos(math.radians(self.attack_angle)) # Thrust calculation on the x plane
		#d_x = self.drag_force * math.cos(math.radians(self.attack_angle)) # drag calculation on the x plane
		#l_x = self.lift_force * math.sin(math.radians(self.attack_angle)) # lift calculation on the x plane
		#f_x = t_x - d_x# - l_x # Total force in x direction
		self.x += delta_x
		self.y -= delta_y

	def draw(self): #spirte print function
		if self.state == True: # check if sprite is alive
			img, img_rect = rot_center(self.sprite, self.rect, self.attack_angle*-1) # sets the rotation of sprite
			gameDisplay.blit(img, (round(self.x), round(self.y))) # prints the sprite


def run():
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
		if play == True: #testing var
			player.move() # simulates one frame of movemnt
		if player.y <= 0: # checks if sprite is too low
			player.y = 0  # sets a floor
		player.draw() # draws the plane

		#DISPLAY UPDATE
		pygame.display.update() # updates the display
		clock.tick(fps) # sets fps

if __name__ == '__main__':
	run()
