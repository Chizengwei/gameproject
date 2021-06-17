from super_mario.data.Info import *
from super_mario.data.tools import *


class Load_Screen:
	def __init__(self):
		self.palyer_img = get_surface(get_image('graphics/mario_bros.png'), 177, 32, 13, 15, (0, 0, 0), 1.2)

	def start(self, game_info):
		self.game_info = game_info
		# 设置玩家初始生命值
		self.info = Info('load_screen', game_info)
		self.next = 'level'
		self.state = 'load'
		self.finished = False
		self.timer = 0
		self.counter = 0
		self.duration = 2000
		pass

	def draw(self, surface):
		surface.fill((0, 0, 0))
		pass

	# TODO 作弊码修改触发机制，此处有BUG
	def update(self, surface, keys, keyUp):
		if self.timer == 0:
			self.timer = pygame.time.get_ticks()
			pass
		elif pygame.time.get_ticks() - self.timer > self.duration:
			self.finished = True
			self.timer = 0
			pass
		self.draw(surface)
		self.info.draw(surface)
		self.info.update()
		surface.blit(self.palyer_img, (150, 140))
		pass

	pass


class GameOver(Load_Screen):
	def start(self, game_info):
		self.game_info = game_info
		self.info = Info('game_over', game_info)
		self.next = 'menu'
		self.finished = False
		self.timer = 0
		self.duration = 4000
		pass

	def update(self, surface, keys, keyUp):
		if self.timer == 0:
			self.timer = pygame.time.get_ticks()
			pass
		elif pygame.time.get_ticks() - self.timer > self.duration:
			self.finished = True
			self.timer = 0
			pass
		self.draw(surface)
		self.info.draw(surface)
		self.info.update()
		pass

	pass
