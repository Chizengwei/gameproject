import json
import os

from super_mario.data import stuff, brick, box
from super_mario.data.Info import *
from super_mario.data.enemy import create_enemy
from super_mario.data.player import Player
from super_mario.data.tools import *


class Level:
	def __init__(self):
		# self.restart()
		self.coin_group = pygame.sprite.Group()
		self.powerup_group = pygame.sprite.Group()
		self.enemy_group_list = {}
		self.dying_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.shell_group = pygame.sprite.Group()
		self.check_point_group = pygame.sprite.Group()
		self.brick_group = pygame.sprite.Group()
		self.box_group = pygame.sprite.Group()
		self.load_sound()

	# 重置精灵组！
	def restart(self):
		self.brick_group.empty()
		self.box_group.empty()
		self.shell_group.empty()
		self.check_point_group.empty()
		self.coin_group.empty()
		self.enemy_group.empty()
		self.powerup_group.empty()
		self.dying_group.empty()
		pass

	def load_sound(self):
		self.trampled_sound = get_sounds('sound/kick.ogg')
		self.transfor_sound = get_sounds('sound/powerup.ogg')

		pass

	def start(self, game_info):
		self.game_info = game_info
		self.player_x = None
		self.info = Info('level', self.game_info)
		self.state = 'level'
		self.next = 'game_over'
		self.set_background()
		self.finished = False
		self.load_map_data()
		self.setup_start_positions()
		self.set_player('mario')
		self.seteup_ground_items()
		self.setup_bricks_and_boxs()
		self.setup_enemy()
		self.setup_check_point()

	def load_map_data(self):
		file_name = 'level_1.json'
		file_path = os.path.join('map', file_name)
		with open(file_path) as f:
			self.map_data = json.load(f)

	def set_background(self):
		self.background = get_image('graphics/level_1.png')
		self.screen = get_surface(self.background, 0, 0, 3692, 224, (0, 0, 0), 1.2)
		self.background_rect = self.screen.get_rect()

		self.game_window = SCREEN.get_rect()
		self.game_ground = pygame.Surface((self.screen.get_width(), self.screen.get_height()))

	def seteup_ground_items(self):
		self.ground_items_group = pygame.sprite.Group()
		for name in ['ground', 'step', 'pipe']:
			for item in self.map_data[name]:
				self.ground_items_group.add(
					stuff.Item(item['x'] * 0.4481, item['y'] * 0.446, item['width'] * 0.446, item['height'] * 0.446,
					           name))
		print(self.ground_items_group)
		pass

	def setup_start_positions(self):
		self.position = []
		for data in self.map_data['maps']:
			self.position.append(
				(data['start_x'] * 0.446, data['end_x'] * 0.446, data['player_x'] * 0.446, data['player_y'] * 0.446))
		(self.start_x, self.end_x, self.player_x, self.player_y) = self.position[0]

	# TODO CHANGE ABILITY
	# 更新关卡代码
	def update(self, surface, keys, keyUp):
		self.current_time = pygame.time.get_ticks()
		# surface.fill(black)
		if self.player.dead:
			if self.current_time - self.player.death_timer > 3000:
				self.finished = True
				self.restart()
				self.update_game_info()
		elif self.is_frozen():
			pass
		else:
			self.update_palyer_position()
			self.check_point()
			self.check_if_go_die()
			self.update_game_window()
			self.info.update()
			self.brick_group.update()
			self.box_group.update()
			self.enemy_group.update(self)
			self.shell_group.update(self)
			self.dying_group.update(self)
			self.powerup_group.update(self)
			self.coin_group.update(self)
		self.player.update(keys, keyUp, surface, self)
		self.draw(surface)
		pass

	def set_player(self, name):
		self.player = Player(name)
		self.player.rect.x = self.game_window.x + self.player_x
		self.player.rect.bottom = self.player_y
		pass

	def update_palyer_position(self):
		self.player.rect.x += self.player.x_vel
		if self.player.rect.x < self.start_x:
			self.player.rect.x = self.start_x
		elif self.player.rect.right > self.end_x:
			self.player.rect.right = self.end_x

		# 这里下面三行代码顺序不能颠倒
		self.check_x_collisions()
		self.player.rect.y += self.player.y_vel
		self.check_y_collisions()

	def update_game_window(self):
		three = self.game_window.x + self.game_window.width / 3
		if self.player.x_vel > 0 and self.player.rect.centerx > three and self.game_window.right < self.end_x:
			self.game_window.x += self.player.x_vel
			self.start_x = self.game_window.x
		pass

	# 关卡绘制代码
	def draw(self, surface):
		# 关键性的，清屏！！！
		self.game_ground.fill(black)
		self.game_ground.blit(self.screen, self.game_window, self.game_window)
		self.game_ground.blit(self.player.image, self.player.rect)
		self.brick_group.draw(self.game_ground)
		self.powerup_group.draw(self.game_ground)
		self.box_group.draw(self.game_ground)
		self.enemy_group.draw(self.game_ground)
		self.shell_group.draw(self.game_ground)
		self.dying_group.draw(self.game_ground)
		self.coin_group.draw(self.game_ground)

		surface.blit(self.game_ground, (0, 0), self.game_window)
		self.info.draw(surface)
		self.info.update()
		pass

	pass

	# 关卡x轴碰撞检测
	def check_x_collisions(self):
		ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
		brick_item = pygame.sprite.spritecollideany(self.player, self.brick_group)
		box_item = pygame.sprite.spritecollideany(self.player, self.box_group)

		# enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
		#
		# if enemy:
		# 	if self.player.big:
		# 		self.player.state = 'big_to_small'
		# 	else:
		# 		self.player.go_die()
		if ground_item:
			self.adjust_player_x(ground_item)
		if brick_item:
			self.adjust_player_x(brick_item)
		if box_item:
			self.adjust_player_y(box_item)

		# enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
		# if enemy:
		# 	if enemy.state != 'death':
		# 		self.player.go_die()

		shell = pygame.sprite.spritecollideany(self.player, self.shell_group)
		if shell:
			if shell.state == 'slide':
				self.player.state = 'big_to_small' if self.player.big else self.player.go_die()
			else:
				if self.player.rect.x < shell.rect.x:
					shell.x_vel = 10
					shell.rect.x += 40
					shell.direction = 1
				else:
					shell.x_vel = -10
					shell.rect.x -= 40
					shell.direction = 0
			shell.state = 'slide'

		powerup = pygame.sprite.spritecollideany(self.player, self.powerup_group)
		if powerup:
			if powerup.name == 'mushroom':
				powerup.kill()
				self.player.state = 'transfiguration'
				self.transfor_sound.play()

			elif powerup.name == 'fire_flower':
				powerup.kill()
				self.player.state = 'big_to_fire'
				self.transfor_sound.play()

			elif powerup.name == 'fire_ball':
				pass
		pass

	# 关卡y轴碰撞检测
	def check_y_collisions(self):
		ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
		if ground_item:
			self.adjust_player_y(ground_item)
		brick_item = pygame.sprite.spritecollideany(self.player, self.brick_group)
		box_item = pygame.sprite.spritecollideany(self.player, self.box_group)

		if brick_item and box_item:
			to_brick = abs(self.player.rect.centerx - (brick_item.rect.centerx + 10))
			to_box = abs(self.player.rect.centerx - (box_item.rect.centerx))
			if to_brick > to_box:
				box_item = None
			else:
				brick_item = None
		if brick_item:
			self.adjust_player_y(brick_item)
		if box_item:
			self.adjust_player_y(box_item)
		self.check_will_fall(self.player)
		enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
		if enemy:
			if self.player.state == 'fall':
				self.enemy_group.remove(enemy)
				if enemy.name == 'koopa':
					self.shell_group.add(enemy)
				else:
					self.dying_group.add(enemy)
				if self.player.y_vel < 0:
					how = 'bumped'
				else:
					how = 'trampled'
					self.player.state = 'jump'
					self.trampled_sound.play()
					self.player.rect.bottom = enemy.rect.top
					self.player.y_vel = self.player.jump_vel * 0.6
				enemy.go_die(how)
		pass

	def adjust_player_x(self, sprite):
		if self.player.rect.left < sprite.rect.left:
			self.player.rect.right = sprite.rect.left
		else:
			self.player.rect.left = sprite.rect.right
		self.player.x_vel = 0
		pass

	def adjust_player_y(self, ground_item):
		if self.player.rect.bottom < ground_item.rect.bottom:
			self.player.y_vel = 0
			self.player.rect.bottom = ground_item.rect.top
			self.player.state = 'walk'
		else:
			self.player.y_vel = 7
			self.player.rect.top = ground_item.rect.bottom
			self.player.state = 'fall'

			self.is_enemy_on(ground_item)

			# TODO 111
			if ground_item.name == 'box' and ground_item.state == 'rest':
				ground_item.go_bump(self)

			if ground_item.name == 'brick':
				if self.player.big and ground_item.brick_type == 0:
					ground_item.smashed(self.dying_group)
				else:
					ground_item.go_bump()

		pass

	def check_will_fall(self, sprite):
		sprite.rect.y += 1
		check_ground = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
		collided = pygame.sprite.spritecollideany(sprite, check_ground)
		if not collided and sprite.state != 'jump' and not self.is_frozen():
			sprite.state = 'fall'
			pass
		sprite.rect.y -= 1
		pass

	def check_if_go_die(self):
		if self.player.rect.y > SCREEN.get_height():
			self.player.go_die()
		pass

	def update_game_info(self):
		if self.player.dead:
			self.game_info['life'] -= 1

		if self.game_info['life'] == 0:
			self.next = 'game_over'
		else:
			self.next = 'load'
		pass

	def setup_bricks_and_boxs(self):
		global x_0, y_0, types
		if 'brick' in self.map_data:
			for brick_data in self.map_data['brick']:
				x, y = brick_data['x'] * 0.446, brick_data['y'] * 0.446
				brick_type = brick_data['type']
				if brick_type == 0:
					if 'brick_num' in brick_data:
						pass
					else:
						self.brick_group.add(brick.Brick(x, y, brick_type, None))
				elif brick_type == 1:
					self.brick_group.add(brick.Brick(x, y, brick_type, self.coin_group))
				else:
					self.brick_group.add(brick.Brick(x, y, brick_type, self.powerup_group))

		if 'box' in self.map_data:
			for box_data in self.map_data['box']:
				x_0, y_0 = box_data['x'] * 0.446, box_data['y'] * 0.446
				types = box_data['type']
				if types == 1:
					self.box_group.add(box.Box(x_0, y_0, types, self.coin_group))
				else:
					self.box_group.add(box.Box(x_0, y_0, types, self.powerup_group))
		pass

	# 设置敌人
	def setup_enemy(self):
		for enemy_group_data in self.map_data['enemy']:
			group = pygame.sprite.Group()
			for enemy_group_id, enemy_list in enemy_group_data.items():
				for enemy_data in enemy_list:
					group.add(create_enemy(enemy_data))
				self.enemy_group_list[enemy_group_id] = group
				pass
		pass

	def setup_check_point(self):
		for item in self.map_data['checkpoint']:
			x, y, w, h, type, = item['x'] * .446, item['y'] * .446, item['width'] * .446, item['height'] * .446, item[
				'type']
			if 'enemy_groupid' in item:
				enemy_groupid = item['enemy_groupid']
			self.check_point_group.add(stuff.Checkpoint(x, y, w, h, type, enemy_groupid))
		pass

	def check_point(self):
		checkpoint = pygame.sprite.spritecollideany(self.player, self.check_point_group)
		if checkpoint:
			if checkpoint.checkpoint_type == 0:
				self.enemy_group.add(self.enemy_group_list[str(checkpoint.enemy_groupid)])
				pass
			checkpoint.kill()

	def is_frozen(self):
		return self.player.state in ['transfiguration', 'big_to_fire', 'fire_to_small', 'big_to_small']

	def is_enemy_on(self, ground_item):
		ground_item.rect.y -= 1
		enemy = pygame.sprite.spritecollideany(ground_item, self.enemy_group)
		if enemy:
			self.enemy_group.remove(enemy)
			self.dying_group.add(enemy)
			if ground_item.rect.centerx > enemy.rect.centerx:
				enemy.go_die('bumped', -1)
			else:
				enemy.go_die('bumped', 1)
		ground_item.rect.y += 1
		pass
