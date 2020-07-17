import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, screen, ai_settings):
		"""Initialize the ship and set its current position"""
		super().__init__()
		
		self.screen = screen
		
		self.ai_settings = ai_settings
		
		self.moving_right = False
		self.moving_left = False
		
		# Load the ship image and get its rect.
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# Start each new ship at the bottom center of the screen.
		self.rect.centerx = float(self.screen_rect.centerx)
		self.rect.bottom = self.screen_rect.bottom
		self.center = float(self.rect.centerx)
		
	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""Deterine the x-coordinate of the ship and draw its image"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		self.rect.centerx = self.center
		self.blitme()
		
	def center_ship(self):
		"""Center the ship"""
		self.center = self.screen_rect.centerx
		
