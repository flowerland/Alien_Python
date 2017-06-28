import pygame
import random
from pygame.sprite import Sprite
class Alien(Sprite):
	def __init__(self,ai_settings,screen,image = 'images/blue.png'):
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		self.image = pygame.image.load(image)
		
		self.rect = self.image.get_rect()
		
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		self.x = float(self.rect.x)
		
	def blitme(self):
		self.screen.blit(self.image,self.rect)
		
	#def update(self):
	#	ran = random.randint(0,1)
		#if ran == 0:
		#	self.x += random.randint(1,5)*self.ai_settings.fleet_direction
		#else:
		#	self.x -= random.randint(1,5)*self.ai_settings.fleet_direction
		#self.rect.x = self.x
	
	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
