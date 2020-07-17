import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Class to represent a bullet"""
	def __init__(self, screen, ship, ai_settings):
		super().__init__()
		self.screen = screen
		
		# Create a bullet rect at (0,0) and set its correct position.
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		# Store the bullet's y-coordinate as a decimal value 
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
	def update(self):
		"""Move the bullet up to the screen"""
		self.y -= self.speed_factor
		self.rect.y = self.y
	
	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
	
