import json

class GameStats():
	"""Track statistics for Alien Invansion"""
	
	def __init__(self, ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		
		# Keep game inactive until player hits PLAY button.
		self.game_active = False
		
		self.read_highscore()
	
	def reset_stats(self):
		"""Initialize statistics that can change during the game"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
		
	def read_highscore(self):
		"""Read high score from the file."""
		
		self.high_score = 0
		try:
			filename = 'data/high_score.json'
			with open(filename) as f_obj:
				content = json.load(f_obj)
			self.high_score = content
		except FileNotFoundError:	
			pass
	
