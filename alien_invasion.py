import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import threading


def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,
	         ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')
	play_button = Button(ai_settings,screen,'Play')
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings,screen,stats)
	
	#创建一个用于存储子弹的编组
	bullets = Group()
	aliens = Group()
	#创建一艘飞船
	ship = Ship(ai_settings,screen)
	#创建一群外星人
	#gf.create_fleet(0,ai_settings,screen,ship,aliens)
	for i in range(4):
		t =threading.Thread(target=gf.create_fleet,args=(i,ai_settings,screen,ship,aliens))
		t.start()
	#开始游戏主循环
	while True:
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,
			aliens,bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
		gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
			play_button)

run_game()
