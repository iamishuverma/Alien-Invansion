import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard
from pygame.sprite import Group
from button import Button

def run_game():
	
	# Initialise game and create a screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.width,ai_settings.height))
	pygame.display.set_caption(ai_settings.title)
	
	# Make the play button.
	play_button = Button(ai_settings,screen,"Play")
	
	# Create an instance to store game statistics and create a scoreboard.
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings,screen,stats)
	
	# Making a ship.
	ship = Ship(screen,ai_settings)
	
	# Making a group to store bullets in.
	bullets = Group()
	
	# Make a group of aliens.
	aliens = Group()	
	
	# Create a fleet of aliens.
	gf.create_fleet(screen,ai_settings,aliens,ship)
	
	# Start the main loop for the game.
	while True:
	
		# Watch for keyboard and mouse events.
		gf.check_events(ship,bullets,screen,ai_settings,play_button,stats,aliens,sb)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(bullets,aliens,ship,ai_settings,screen,stats,sb)
			gf.update_aliens(ai_settings,aliens,ship,stats,screen,bullets,sb)
			
		# Update the screen with background color and ship image.
		gf.update_screen(screen,ai_settings,ship,bullets,aliens,play_button,stats,sb)
		
run_game()
