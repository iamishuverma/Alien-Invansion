import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, screen, ai_settings):
		super().__init__()
		
		self.screen = screen
		self.ai_settings = ai_settings
		
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		# Implementing colorkey transparency.
		color = (230, 230, 230)
		self.image.set_colorkey(color)
		
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		self.x = float(self.rect.x)
	
	def blitme(self):
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""Move the alien left or right"""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x
	
	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if(self.rect.right >= screen_rect.right):
			return True
		elif(self.rect.left <= 0):
			return True
		
		
		
