import pygame

from super_mario.data import tools
from super_mario.data.tools import SCREEN


# TODO 333
def create_powerup(centerx, centery, type):
	"""as 用多态技术产生不同的类型对象"""
	obj = None
	if type == 3:
		obj = Mushroom(centerx, centery)
	elif type == 1:
		pass
	elif type == 4:
		obj = Fire_flower(centerx, centery)
	return obj


class PowerUp(pygame.sprite.Sprite):
	def __init__(self, centerx, centery, frame_rects, types=0):
		pygame.sprite.Sprite.__init__(self)
		self.frames = []
		self.frame_index = 0
		for frame_rect in frame_rects:
			self.frames.append(
				tools.get_surface(tools.get_image('graphics/item_objects.png'), *frame_rect, (0, 0, 0), 1))
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery

		self.origin_y = self.rect.top

		self.x_vel = 0
		self.direction = 1
		self.y_vel = -1
		self.gravity = 1
		self.max_y_vel = 8

	def update(self, level):
		self.current_time = pygame.time.get_ticks()
		self.handle_state(level)
		self.image = self.frames[self.frame_index]
		self.update_position(level)
		pass

	def handle_state(self, level):
		if self.state == 'walk':
			self.walk()
		if self.state == 'fall':
			self.fall()
		if self.state == 'grow':
			self.grow()
		pass

	def walk(self):
		self.rect.x += self.x_vel
		pass

	def fall(self):
		pass

	def update_position(self, level):
		self.rect.x += self.x_vel
		self.check_x_collisions(level)
		self.rect.y += self.y_vel
		self.check_y_collisions(level)

		if self.rect.x < 0 or self.rect.y > SCREEN.get_height():
			self.kill()
		pass

	def check_x_collisions(self, level):
		check_group = pygame.sprite.Group(level.ground_items_group)
		sprite = pygame.sprite.spritecollideany(self, check_group)
		if sprite:
			# self.direction = 1 if self.direction == 0 else 0
			if self.direction:  # 向右
				self.direction = 0
				self.rect.right = sprite.rect.left
			else:
				self.direction = 1
				self.rect.left = sprite.rect.right
			self.x_vel *= -1

		pass

	def check_y_collisions(self, level):
		check_ground = pygame.sprite.Group(level.ground_items_group, level.box_group, level.brick_group)
		sprite = pygame.sprite.spritecollideany(self, check_ground)
		if sprite:
			if self.rect.top < sprite.rect.top:
				self.rect.bottom = sprite.rect.top
				self.y_vel = 0
				self.state = 'walk'
		level.check_will_fall(self)
		pass

	def grow(self):
		pass


class Mushroom(PowerUp):
	def __init__(self, centerx, centery):
		PowerUp.__init__(self, centerx, centery, [(0, 0, 16, 16)])
		print('values')
		self.x_vel = 1.5
		self.state = 'grow'
		self.name = 'mushroom'

	def update(self, level):
		if self.state == 'grow':
			self.rect.y += self.y_vel
			if self.rect.bottom < self.origin_y:
				self.state = 'walk'
			pass
		elif self.state == 'walk':
			pass
		elif self.state == 'fall':
			if self.y_vel < self.max_y_vel:
				self.y_vel += self.gravity
		if self.state != 'grow':
			self.update_position(level)
		pass


class Fire_flower(PowerUp):
	def __init__(self, centerx, centery):
		frame_rects = [(0, 32, 16, 16), (16, 32, 16, 16), (32, 32, 16, 16), (48, 32, 16, 16)]
		PowerUp.__init__(self, centerx, centery, frame_rects)
		print('values')
		self.x_vel = 1.5
		self.state = 'grow'
		self.name = 'fire_flower'
		self.timer = 0

	def update(self, level):
		if self.state == 'grow':
			self.rect.y += self.y_vel
			if self.rect.bottom < self.origin_y:
				self.state = 'rest'
		self.current_time = pygame.time.get_ticks()
		if self.timer == 0:
			self.timer = self.current_time
		elif self.current_time - self.timer > 30:
			self.frame_index += 1
			self.frame_index %= len(self.frames)
			self.timer = self.current_time
			self.image = self.frames[self.frame_index]
		pass

	pass


class Fire_ball(PowerUp):
	def __init__(self, centerx, centery, direction=1):
		frame_rects = [(96, 144, 8, 8), (104, 144, 8, 8), (96, 152, 8, 8), (104, 152, 8, 8), (112, 144, 16, 16),
		               (112, 160, 16, 16), (112, 176, 16, 16)]
		super().__init__(centerx, centery, frame_rects)

		self.name = 'fireball'
		self.state = 'fly'
		self.direction = direction
		self.x_vel = 10 if self.direction else -10
		self.y_vel = 1
		self.gravity = 1
		self.timer = 0

	def update(self, level):
		self.current_time = pygame.time.get_ticks()
		if self.state == 'fly':
			self.y_vel += self.gravity*.4
			# if level.player.d
			self.x_vel += level.player.x_vel*.3
			if self.current_time - self.timer > 200:
				self.frame_index += 1
				self.frame_index %= 4
				self.timer = self.current_time
				self.image = self.frames[self.frame_index]
			self.update_position(level)
		elif self.state == 'boom':
			if self.current_time - self.timer > 50:
				if self.frame_index < 6:
					self.frame_index += 1
					self.timer = self.current_time
					self.image = self.frames[self.frame_index]
				else:
					self.kill()
		pass

	def update_position(self, level):
		self.rect.x += self.x_vel
		self.check_x_collisions(level)
		self.rect.y += self.y_vel
		self.check_y_collisions(level)
		if self.rect.x < 0 or self.rect.y > SCREEN.get_height():
			self.kill()
		pass

	def check_x_collisions(self, level):
		check_group = pygame.sprite.Group(level.ground_items_group)
		sprite = pygame.sprite.spritecollideany(self, check_group)
		if sprite:
			if self.direction:  # 向右
				self.direction = 0
				self.rect.right = sprite.rect.left
			else:
				self.direction = 1
				self.rect.left = sprite.rect.right
			self.x_vel *= -1

		pass

	def check_y_collisions(self, level):
		check_ground = pygame.sprite.Group(level.ground_items_group, level.box_group, level.brick_group)
		sprite = pygame.sprite.spritecollideany(self, check_ground)
		kill_enemy = pygame.sprite.spritecollideany(self, level.enemy_group)
		if sprite:
			self.state = 'boom'
		pass

		if kill_enemy:
			self.state = 'boom'
			level.enemy_group.remove(kill_enemy)
			level.dying_group.add(kill_enemy)
			kill_enemy.go_die('bumped')

	pass


class LifeMushroom(PowerUp):
	pass


class Star(PowerUp):
	pass
