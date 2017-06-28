import sys
import pygame
import random
from bullet import Bullet
from alien import Alien
import time
import threading

lock = threading.RLock()
def check_keydown_events(event,ai_settings,screen,ship,bullets):
	'''响应按键'''
	if event.key==pygame.K_ESCAPE:
		print ("exit")
		sys.exit()
		pygame.quit()
	elif event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)

def check_keyup_events(event,ship):
	'''响应松开'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
	bullets):
	#监视键盘和鼠标事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,
			ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
	bullets,mouse_x,mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		#重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		aliens.empty()
		bullets.empty()
		
		#create_fleet(0,ai_settings,screen,ship,aliens)
		for i in range(4):
			t =threading.Thread(target=create_fleet,args=(i,ai_settings,screen,ship,aliens))
			t.start()
		ship.center_ship()
		
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	#screen.fill(ai_settings.bg_color)
	screen.blit(ai_settings.bg_image, (0, 0)) 
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()
	
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	'''更新子弹的位置，并删除已消失的子弹'''
	bullets.update()
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,
		ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
	aliens,bullets):
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	#lock.acquire()
	if len(aliens) == 0 and threading.activeCount() == 1:
		#print(threading.activeCount())
		#print(threading.currentThread().getName() + " start")
		bullets.empty()
		ai_settings.increase_speed()
		#提高等级
		stats.level += 1
		sb.prep_level()
		#create_fleet(0,ai_settings,screen,ship,aliens)
		for i in range(4):
			t =threading.Thread(target=create_fleet,args=(i,ai_settings,screen,ship,aliens))
			t.start()
		#print(threading.currentThread().getName() + " end")
	#lock.release()
	
	
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets) < ai_settings.bulltes_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def create_fleet(i,ai_settings,screen,ship,aliens):
	time.sleep(i)
	alien1 = Alien(ai_settings,screen,ai_settings.image1)
	alien5 = Alien(ai_settings,screen,ai_settings.image5)
	number_aliens_x = get_number_aliens_x(ai_settings,alien1.rect.width)
	#number_rows = get_number_rows(ai_settings,ship.rect.height,
	#	alien1.rect.height)
	#number_rows = 2
	row_number = 1
	alien_number = 1
	while alien_number < random.randint(1,3):
		create_alien(ai_settings,screen,aliens,alien_number,
			number_aliens_x)
		alien_number += 1
	
	#create_alien(ai_settings,screen,aliens,alien_number,
	#		row_number)
	#创建一群星人
	#for row_number in range(random.randint(0,number_rows)):
	#	for alien_number in range(random.randint(0,number_aliens_x)):
	#		create_alien(ai_settings,screen,aliens,alien_number,
	#			row_number)

def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2*alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	lock.acquire()
	#print(threading.currentThread().getName() + " start")
	alien1 = Alien(ai_settings,screen,ai_settings.image1)
	alien2 = Alien(ai_settings,screen,ai_settings.image2)
	alien3 = Alien(ai_settings,screen,ai_settings.image3)
	alien4 = Alien(ai_settings,screen,ai_settings.image4)
	alien = [alien1,alien2,alien3,alien4]
	i = random.randint(0,3)
	alien_width = alien[i].rect.width
	alien[i].x = alien_width + 2*alien_width*random.randint(0,row_number)
	alien[i].rect.x = alien[i].x
	#alien[i].rect.y = alien[i].rect.height + 2 * alien[i].rect.height * row_number
	alien[i].rect.y = alien[i].rect.height
	aliens.add(alien[i])
	#print(threading.currentThread().getName() + " end")
	lock.release()

def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y = (ai_settings.screen_height - (3*alien_height) -
		ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	#for alien in aliens.sprites():
	#	alien.update()
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
	check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
	change_fleet_direction(ai_settings,aliens)
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed*ai_settings.alien_speed_factor
	ai_settings.fleet_direction *= -1			

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
	
		#create_fleet(0,ai_settings,screen,ship,aliens)
		for i in range(4):
			t =threading.Thread(target=create_fleet,args=(i,ai_settings,screen,ship,aliens))
			t.start()
		ship.center_ship()
	
		time.sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
			break

def check_high_score(stats,sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
