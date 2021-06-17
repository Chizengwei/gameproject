import super_mario.data.tools
from super_mario.data import tools
from super_mario.data.tools import *

enemy = None
ENEMY_SPEED = 1
GRAVITY = 4
FRICTION = 0.12


def create_enemy(enemy_data):
	global enemy
	enemy_type = enemy_data['type']
	x, y_bottom, direction, color = enemy_data['x'] * 0.446, enemy_data['y'] * 0.446, enemy_data['direction'], \
	                                enemy_data['color']

	if enemy_type == 0:  # 蘑菇怪
		enemy = Goomba(x, y_bottom, direction, 'goomba', color)
	elif enemy_type == 1:  # 乌龟怪
		enemy = Koopa(x, y_bottom, direction, 'koopa', color)
	return enemy


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y_bottom, direction, name, frame_rects):
		pygame.sprite.Sprite.__init__(self)
		self.direction = direction
		self.name = name
		self.frame_index = 0
		self.left_frames = []
		self.right_frames = []
		self.fall_frames = []
		self.img = get_image('graphics/enemies.png')

		self.load_frames(frame_rects)
		self.frames = self.left_frames if self.direction == 0 else self.right_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.bottom = y_bottom

		self.timer = 0
		self.x_vel = -1 * ENEMY_SPEED if self.direction == 0 else ENEMY_SPEED
		self.y_vel = 0
		self.gravity = GRAVITY
		self.state = 'walk'
		self.face_right = False
		self.death_timer = 0

	pass

	def load_frames(self, frame_rects):
		for frame_rect in frame_rects:
			left_frame = get_surface(self.img, *frame_rect, (0, 0, 0), 1)
			right_frame = pygame.transform.flip(left_frame, True, False)
			fall_death_frame = pygame.transform.rotate(left_frame, 180)
			self.left_frames.append(left_frame)
			self.right_frames.append(right_frame)
			self.fall_frames.append(fall_death_frame)
		pass

	# 更新状态
	def update(self, level):
		self.current_time = pygame.time.get_ticks()
		self.handle_state(level)
		if self.current_time - self.timer > 125 and self.state == 'walk':
			self.frame_index = (self.frame_index + 1) % 2
			self.timer = self.current_time
		elif self.state == 'death' and self.y_vel > 0:
			self.frames = self.fall_frames
		self.image = self.frames[self.frame_index]
		self.update_position(level)
		pass

	# 处理怪物当前状态
	def handle_state(self, level):
		if self.state == 'walk':
			self.walk()
		if self.state == 'fall':
			self.fall()
		if self.state == 'death':
			self.die()
		if self.state == 'trampled':
			self.trampled(level)
			pass
		if self.face_right:
			self.frames = self.right_frames
		else:
			self.frames = self.left_frames
		pass

	# 怪物被踩扁死亡
	def trampled(self, level):
		pass

	def walk(self):
		self.x_vel = -ENEMY_SPEED if self.direction == 0 else ENEMY_SPEED
		pass

	def fall(self):
		if self.y_vel < 10:
			self.y_vel += GRAVITY
		pass

	def die(self):
		self.rect.x += self.x_vel
		self.rect.y += self.y_vel
		self.y_vel += self.gravity
		if self.rect.y > tools.SCREEN.get_width():
			self.kill()
		pass

	def go_die(self, how, direction=1):
		self.death_timer = self.current_time
		if how in ['bumped', 'slide']:
			self.x_vel = ENEMY_SPEED * direction
			self.y_vel = -8
			self.gravity = 0.8
			self.state = 'death'
			self.frame_index = 0
		elif how == 'trampled':
			self.frame_index = 2
			self.state = 'trampled'

			pass

	def update_position(self, level):
		self.rect.x += self.x_vel
		self.check_x_collisions(level)
		self.rect.y += self.y_vel
		if self.state != 'death' and level.player.state != 'death':
			self.check_y_collisions(level)
		pass

	def check_x_collisions(self, level):
		check_group = pygame.sprite.Group(level.ground_items_group)
		sprite = pygame.sprite.spritecollideany(self, check_group)
		is_die = pygame.sprite.spritecollideany(level.player, level.enemy_group)

		if sprite:
			# self.direction = 1 if self.direction == 0 else 0
			if self.direction:  # 向右
				self.direction = 0
				self.rect.right = sprite.rect.left
			else:
				self.direction = 1
				self.rect.left = sprite.rect.right
			self.x_vel *= -1
		if is_die:
			if level.player.hurt_immune:
				return
			elif level.player.big:
				level.player.state = 'big_to_small'
				level.player.hurt_immune = True
			else:
				level.player.go_die()
		if self.state == 'slide':
			enemy_pump = pygame.sprite.spritecollideany(self, level.enemy_group)
			if enemy_pump:
				enemy_pump.go_die(how='slide', direction=self.direction)
				level.enemy_group.remove(enemy_pump)
				level.dying_group.add(enemy_pump)

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


class Goomba(Enemy):
	def __init__(self, x, y, direction, name, color):
		bright_frames = [(0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16)]
		dark_frames = [(0, 48, 16, 16), (16, 48, 16, 16), (32, 48, 16, 8)]
		if not color:
			frame_rects = bright_frames
		else:
			frame_rects = dark_frames

		Enemy.__init__(self, x, y, direction, name, frame_rects)
		pass

	def trampled(self, level):
		self.x_vel = 0
		self.frame_index = 2

		# self.image = self.frames[self.frame_index]
		if self.death_timer == 0:
			self.death_timer = self.current_time
		elif (self.current_time - self.death_timer) % 100 < 50:
			self.image = pygame.Surface((16, 16))
		elif self.current_time - self.death_timer > 500:
			self.kill()
		pass


class Koopa(Enemy):
	def __init__(self, x, y, direction, name, color):
		bright_frames = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]
		dark_frames = [(96, 72, 16, 22), (112, 72, 16, 22), (160, 72, 16, 22)]
		if not color:
			frame_rects = bright_frames
		else:
			frame_rects = dark_frames
		Enemy.__init__(self, x, y, direction, name, frame_rects)
		self.shell_timer = 0

	def trampled(self, level):
		self.x_vel = 0
		self.frame_index = 2

		if self.shell_timer == 0:
			self.shell_timer = self.current_time
		if self.current_time - self.shell_timer > 5000:
			self.state = 'walk'
			level.enemy_group.add(self)
			level.shell_group.remove(self)
			self.shell_timer = 0
		pass

	def handle_state(self, level):
		super().handle_state(level)
		if self.state == 'slide':
			self.slide(level)
			pass

	def slide(self, level):
		self.x_vel -= FRICTION
		if self.x_vel == 0:
			self.x_vel = 0
		pass
