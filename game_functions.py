import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ship, bullets, screen, ai_settings, play_button, stats, aliens, sb):
	"""Respond to key presses and mouse events"""
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			sys.exit()
		elif(event.type == pygame.MOUSEBUTTONDOWN):						# If mouse button is clicked.
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(play_button,mouse_x,mouse_y,stats,ship,bullets,aliens,ai_settings,screen,sb)
		
		elif(event.type == pygame.KEYDOWN):								# If the event if a keypress.
			check_keydown_events(event,ship,screen,ai_settings,bullets)
			
		elif(event.type == pygame.KEYUP):								# If the event is keyreleased.
			check_keyup_events(event,ship)
			
def update_screen(screen, ai_settings, ship, bullets, aliens, play_button, stats, sb):
	"""Set the background color, display the ship image and make screen visible"""
	
	# Redraw the screen during each pass through the loop.
	screen.fill(ai_settings.bg_color)
	
	# Draw bullets to the screen.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	# Displaying ship to the screen.
	ship.blitme()
	
	# Displaying aliens to the screen.
	aliens.draw(screen)
	
	# Draw the play button only when the game is inactive.
	if not stats.game_active:
		play_button.draw_button()
	
	# Draw the score.
	sb.show_score()
	
	# Make the most recently drawn screen visible.
	pygame.display.flip()
	
def check_play_button(play_button, mouse_x, mouse_y, stats, ship, bullets, aliens, ai_settings, screen, sb):
	"""Start a new game when the user clicks Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game settings.
		ai_settings.initialize_dynamic_settings()
		
		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		
		sb.prep_score()
		sb.prep_level()
		sb.prep_ships()
		
		stats.game_active = True
		
		# Empty the lists of aliens and bullets.
		aliens.empty()
		bullets.empty()
		
		# Create a new fleet and center the ship.
		create_fleet(screen,ai_settings,aliens,ship)
		ship.center_ship()
		
def check_keydown_events(event, ship, screen, ai_settings, bullets):
	if(event.key == pygame.K_RIGHT):							# If RIGHT key is pressed.
		# Move the ship to the right
		ship.moving_right = True
	elif(event.key == pygame.K_LEFT):							# If LEFT key is pressed.
		# Move the ship to the left
		ship.moving_left = True
	elif(event.key == pygame.K_SPACE):							# If SPACE bar is pressed.
		fire_bullet(bullets,ai_settings,screen,ship)
	elif(event.key == pygame.K_q):
		sys.exit()

def check_keyup_events(event,ship):
	if(event.key == pygame.K_RIGHT):							# If RIGHT key is released.
		# Stop moving the ship to the right
		ship.moving_right = False
	elif(event.key == pygame.K_LEFT):							# If LEFT key is released.
		# Stop moving the ship to the left
		ship.moving_left = False
		
def update_bullets(bullets, aliens, ship, ai_settings, screen, stats, sb):
	# Update the positions of all bullets
	bullets.update()
	
	check_bullet_alien_collisions(bullets,aliens,ship,ai_settings,screen,stats,sb)
	
	# Get rid of bullets that have disappeared.
	for bullet in bullets.copy():
		if(bullet.rect.bottom <= 0):
			bullets.remove(bullet)
	
def check_bullet_alien_collisions(bullets, aliens, ship, ai_settings, screen, stats, sb):
	# Detecting collisions between bullets and aliens and deleting both of them if there is a collision.
	collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collision:
		for aliens in collision.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
		
	if(len(aliens) == 0):
		# If the entire fleet is destroyed, start a new level.
		bullets.empty()
		ai_settings.increase_speed()
		
		# Increase level.
		stats.level += 1
		sb.prep_level()
		
		create_fleet(screen,ai_settings,aliens,ship)
	
def fire_bullet(bullets, ai_settings, screen, ship):
	if(len(bullets) < ai_settings.bullets_allowed):
		# Fire the bullet
		new_bullet = Bullet(screen,ship,ai_settings)
		bullets.add(new_bullet)
		
def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row"""	
	available_space_x = ai_settings.width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x	
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen."""
	available_space_y = (ai_settings.height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def create_alien(screen, ai_settings, aliens, alien_number, row_number):
	"""Create an alien and place it in a row"""
	alien = Alien(screen,ai_settings)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 50 + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def create_fleet(screen, ai_settings, aliens, ship):
	"""Create a full fleet of aliens"""
	# Create an alien and find the number of aliens in a row.
	# Spacing between each alien is equal to one alien width.
	alien  = Alien(screen,ai_settings)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)		
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	# Create the first row of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(screen,ai_settings,aliens,alien_number,row_number)
		
def update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb):
	check_fleet_edges(ai_settings,aliens)
	
	aliens.update()		
	
	# Look for aliens-ship collisions.
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,aliens,ship,stats,screen,bullets,sb)
	
	# Look for aliens hitting the bottom of the screen.
	check_aliens_bottom(ai_settings,aliens,ship,stats,screen,bullets,sb)
	
def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, aliens, ship, stats, screen, bullets, sb):
	
	if(stats.ships_left > 0):
		stats.ships_left -= 1
		sb.prep_ships()
		
		aliens.empty()
		bullets.empty()
	
		create_fleet(screen,ai_settings,aliens,ship)
		ship.center_ship()
	
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings, aliens, ship, stats, screen, bullets, sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings,aliens,ship,stats,screen,bullets,sb)
			break
			
def check_high_score(stats, sb):
	"""Check to se if there's a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
