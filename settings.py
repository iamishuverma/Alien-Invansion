class Settings():
	"""A class to store all setting for Alien Invansion."""
	def __init__(self):
	
		# Game settings.
		self.height = 600
		self.width = 1200
		self.title = "Alien Invansion"
		
		# Ship settings.
		self.ship_limit = 3
		
		# Bullet settings.
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 255,255,255
		self.bullets_allowed = 5
		
		# Alien settings.
		self.fleet_drop_speed = 10
		
		# How quickly the game speeds up.
		self.speedup_scale=1.1
		# How quickly the alien point values increase
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		"""Initialize settings that change through out the game."""	

		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_direction = 1					# 1 represents RIGHT, -1 represents LEFT
		self.alien_points = 50
		
	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)		
