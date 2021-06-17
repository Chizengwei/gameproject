from super_mario.data.Info import *

from super_mario.data.Info import Info
from super_mario.data.tools import *


class MainMenu:
	def __init__(self):
		self.counter = 0
		self.cheat = False
		self.game_info = {
			'score': 0,
			'coin': 0,
			'life': 3,
			'player_state': 'small'
		}
		self.start(self.game_info)
		pass

	# TODO 作弊码具体逻辑包括但不限于无敌，增加生命等等,后续逐渐更改
	def cheat_code(self, key):
		# self.game_info['life'] += 100
		# 增加生命作弊码
		if pygame.KEYDOWN:
			if key == pygame.K_UP and self.counter == 0:
				self.counter += 2
				print(self.counter)
			elif key == pygame.K_DOWN and self.counter == 2:
				self.counter += 2
			elif key == pygame.K_LEFT and self.counter == 4:
				self.counter += 3
				print(self.counter)
			elif key == pygame.K_RIGHT and self.counter == 7:
				self.counter += 4
				print(self.counter)
			elif key == pygame.K_a and self.counter == 11:
				self.counter += 5
				print(self.counter)
			elif key == pygame.K_d and self.counter == 16:
				self.counter += 6
				print(self.counter)
			elif key == pygame.K_a and self.counter == 22:
				self.counter += 7
				print(self.counter)
			elif key == pygame.K_d and self.counter == 29:
				self.counter += 8
				print(self.counter)
			elif key != pygame.K_a and key != pygame.K_RIGHT and key != pygame.K_d and key != pygame.K_UP and key != pygame.K_DOWN and key != pygame.K_LEFT:
				self.counter = 0

	# print(self.game_info['life'] + "success changed life")

	pass

	def start(self, game_info):
		self.game_info = game_info
		# 初始化主菜单内容！！
		self.titleScreen = get_surface(get_image('graphics/title_screen.png'), 1, 60, 176, 88, (255, 0, 220), 1.2)
		self.screen = get_surface(get_image('graphics/level_1.png'), 0, 0, 3692, 224, (0, 0, 0), 1.2)
		self.start_sound = get_sounds('sound/pipe.ogg')
		self.select_sound = get_sounds('sound/coin.ogg')
		self.cursor = pygame.sprite.Sprite()
		self.info = Info('main_info', self.game_info)
		self.set_cursor()
		# self.set_background()
		self.set_palyer()
		self.finished = False
		self.state = 'menu'
		self.next = 'load'

	# 设置主菜单背景
	def set_background(self):
		pass

	# 设置主菜单玩家
	def set_palyer(self):
		pic = get_image('graphics/mario_bros.png')
		self.palyerScreen = get_surface(pic, 177, 32, 14, 16, (0, 0, 0), 1.2)

	# 设置主菜单光标
	def set_cursor(self):
		self.cursor.image = get_surface(get_image('graphics/item_objects.png'), 24, 160, 8, 8, (0, 0, 0), 1.2)
		rect = self.cursor.image.get_rect()
		rect.x, rect.y = (120, 162)
		self.cursor.rect = rect
		self.cursor.state = '1P'

	# 更新主菜单光标
	def update_cursor(self, keys):
		if keys == pygame.K_UP:
			# self.select_sound.play()
			self.cursor.state = '1P'
			self.cursor.rect.y = 162
		elif keys == pygame.K_DOWN:
			# self.select_sound.play()
			self.cursor.state = '2P'
			self.cursor.rect.y = 181
		elif keys == pygame.K_RETURN:

			if self.cursor.state == '1P':
				self.finished = True
				self.start_sound.play()
				self.reset_game_info()
			elif self.cursor.state == '2P':
				self.start_sound.play()
				self.finished = True
				self.reset_game_info()
				pass
			pass
		pass

	# get_keys不是同步状态
	def update(self, surface, keys, keyUp):
		self.cheat_code(keys)
		if self.counter == 37:
			self.game_info['life'] = 100
			print("success changed life")
			print(self.game_info['life'])
			self.counter = 0
			self.cheat = True
		self.update_cursor(keys)
		surface.blit(self.screen, (0, 0))
		surface.blit(self.titleScreen, (
			95, 45))
		surface.blit(self.palyerScreen, (50, 220))
		self.info.update()
		surface.blit(self.cursor.image, self.cursor.rect)
		self.info.draw(surface)

	def reset_game_info(self):
		if self.cheat:
			self.game_info.update({
				'score': 0,
				'coin': 0,
				'life': 100,
				'player_state': 'small'
			})
		else:
			self.game_info.update({
				'score': 0,
				'coin': 0,
				'life': 3,
				'player_state': 'small'
			})
		pass
