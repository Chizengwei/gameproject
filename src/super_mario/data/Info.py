import pygame.font

from super_mario.data.coin import *


def create_label(label, size=20, width_scale=1.2, height_scale=1):
	# self.string = label
	# 设置字体文件，和字体大小
	font = pygame.font.Font('font/simhei.ttf', (int)(size * .8))

	label_image = font.render(label, True, (255, 255, 255))
	return label_image
	pass


class Info:
	def __init__(self, state, game_info):
		self.game_info = game_info
		self.stateLabels = []
		self.count = 0
		self.state = state
		self.create_states_labels()
		self.coin = FlashCoin()
		self.create_info_labels()

	def create_states_labels(self):
		if self.state == 'main_info':
			self.stateLabels.append(create_label('1  PLAYER  游戏'))
			self.stateLabels.append(create_label('2  PLAYER  游戏'))
			self.stateLabels.append(create_label('最高分   -'))
			self.stateLabels.append(create_label('000000'))
			self.stateLabels.append(create_label('MARIO'))
			self.stateLabels.append(create_label('关卡'))
			self.stateLabels.append(create_label('计时器'))
			self.stateLabels.append(create_label('0 - 0'))
			self.stateLabels.append(create_label(' X00'))
			return self.stateLabels
		elif self.state == 'level':
			self.stateLabels.append(create_label('马里奥'))
			self.stateLabels.append(create_label('计时器'))
			self.stateLabels.append(create_label(' x{}'.format(self.game_info['coin'])))
			return self.stateLabels
			pass
		elif self.state == 'load_screen':
			# self.stateLabels.append(create_label('1  PLAYER  GAME'))
			# self.stateLabels.append(create_label('2  PLAYER  GAME'))
			# self.stateLabels.append(create_label('TOP -'))
			# self.stateLabels.append(create_label('000000'))
			self.stateLabels.append(create_label('马里奥'))
			self.stateLabels.append(create_label('关卡'))
			self.stateLabels.append(create_label('计时器'))
			self.stateLabels.append(create_label('1 - 1'))
			self.stateLabels.append(create_label(' x {}'.format(self.game_info['coin'])))
			self.stateLabels.append(create_label('  ×   {}'.format(self.game_info['life'])))
			return self.stateLabels
			pass
		elif self.state == 'game_over':
			self.stateLabels.append(create_label('马里奥'))
			self.stateLabels.append(create_label('游戏结束，从头再来'))
			self.stateLabels.append(create_label('计时器'))
			self.stateLabels.append(create_label(' X00'))
			return self.stateLabels
			pass
		pass

	def create_info_labels(self):
		pass

	def update(self):
		self.coin.update()
		pass

	def draw(self, surface):
		if self.state == 'main_info':
			surface.blit(self.stateLabels[0], (140, 160))
			surface.blit(self.stateLabels[1], (140, 180))
			surface.blit(self.stateLabels[2], (130, 205))
			surface.blit(self.stateLabels[3], (220, 205))
			surface.blit(self.stateLabels[3], (30, 25))
			surface.blit(self.stateLabels[4], (30, 10))
			surface.blit(self.stateLabels[5], (230, 10))
			surface.blit(self.stateLabels[6], (330, 10))
			surface.blit(self.stateLabels[7], (230, 25))
			surface.blit(self.stateLabels[8], (150, 25))
			surface.blit(self.coin.image, self.coin.rect)
		elif self.state == 'load_screen':
			# surface.blit(self.stateLabels[0], (140, 160))
			# surface.blit(self.stateLabels[1], (140, 180))
			# surface.blit(self.stateLabels[2], (160, 205))
			# surface.blit(self.stateLabels[3], (200, 205))
			surface.blit(self.stateLabels[0], (30, 25))
			surface.blit(self.stateLabels[1], (140, 110))
			surface.blit(self.stateLabels[2], (300, 25))
			surface.blit(self.stateLabels[3], (220, 110))
			surface.blit(self.stateLabels[4], (self.coin.rect.x + 10, self.coin.rect.y))
			surface.blit(self.stateLabels[5], (200, 140))
			# surface.blit(self.stateLabels[5], (150, 25))
			surface.blit(self.coin.image, self.coin.rect)
			pass
		elif self.state == 'level':
			surface.blit(self.stateLabels[0], (30, 25))
			surface.blit(self.stateLabels[1], (300, 25))
			surface.blit(self.stateLabels[2], (self.coin.rect.x + 10, self.coin.rect.y))
			surface.blit(self.coin.image, self.coin.rect)
			pass
		elif self.state == 'game_over':
			surface.blit(self.stateLabels[0], (30, 25))
			surface.blit(self.stateLabels[1], (150, 150))
			surface.blit(self.stateLabels[2], (300, 25))
			surface.blit(self.stateLabels[3], (self.coin.rect.x + 10, self.coin.rect.y))
			surface.blit(self.coin.image, self.coin.rect)

	pass
