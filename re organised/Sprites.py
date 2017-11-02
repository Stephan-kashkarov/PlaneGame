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

