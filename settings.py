import pygame
import random

class Settings():
	def __init__(self):
		
		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		self.bg_image = pygame.image.load('images/sky.png')
		
		#子弹设置
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 0,191,255
		self.bulltes_allowed = 8
		
		#外星人设置
		self.fleet_drop_speed = 1
		self.speedup_scale = 1.1
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
		self.image1 = 'images/blue.png'
		self.image2 = 'images/green.png'
		self.image3 = 'images/red.png'
		self.image4 = 'images/orange.png'
		self.image5 = 'images/earth.png'
		
		self.ship_limit = 3

	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 2.5
		self.alien_speed_factor = 1
		self.bullet_speed_factor = 3
		self.fleet_direction = 1
		#记分
		self.alien_points = 50

	def increase_speed(self):
		if self.ship_speed_factor < 6:
			self.ship_speed_factor *= self.speedup_scale
		if self.alien_speed_factor < 3:
			self.alien_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		#self.alien_points = int(self.alien_points * self.score_scale)
