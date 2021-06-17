import super_mario.data.powerup
from super_mario.data import powerup
from super_mario.data.tools import *

GRAVIIRY = 5


class Box(pygame.sprite.Sprite):

	def __init__(self, x, y, box_type, group, color=0, name='box'):
		pygame.sprite.Sprite.__init__(self)
		self.gravity = GRAVIIRY
		self.state = 'rest'
		self.img = get_image('graphics/tile_set.png')
		self.timer = 0
		self.group = group
		self.x = x
		self.y = y
		self.box_type = box_type
		light_rect_frames = [(384, 0, 16, 16), (400, 0, 16, 16), (416, 0, 16, 16), (432, 0, 16, 16)]
		dark_rect_frames = [(384, 32, 16, 16), (400, 32, 16, 16), (416, 32, 16, 16), (432, 0, 16, 16)]

		if not color:
			self.frame_rects = light_rect_frames
		else:
			self.frame_rects = dark_rect_frames

		self.frames = []
		for frame_rect in self.frame_rects:
			self.frames.append(get_surface(get_image('graphics/tile_set.png'), *frame_rect, (0, 0, 0), 1.25))
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		self.name = name
		self.y_vel = 0

	def update(self):
		self.current_time = pygame.time.get_ticks()
		self.handle_state()
		self.image = self.frames[self.frame_index]

	pass

	def handle_state(self):
		if self.state == 'rest':
			self.rest()
		if self.state == 'bumped':
			self.bumped()
		if self.state == 'open':
			self.open()
		if self.state == 'fall':
			self.fall()
		pass

	def rest(self):
		frame_durations = [375, 150, 150]
		count = self.current_time - self.timer
		if self.timer == 0:
			self.timer = self.current_time
		elif count > frame_durations[self.frame_index]:
			self.frame_index += 1
			self.frame_index %= 3
			self.timer = self.current_time
		pass

	def go_bump(self, level):
		if self.box_type == 1:
			pass
		elif not level.player.big and (self.box_type == 4 or self.box_type == 3):
			self.group.add(powerup.create_powerup(self.rect.centerx, self.rect.centery, 3))
			pass
		elif level.player.big and self.box_type == 3:
			self.group.add(powerup.create_powerup(self.rect.centerx, self.rect.centery, 4))
			pass
		else:
			self.group.add(powerup.create_powerup(self.rect.centerx, self.rect.centery, self.box_type))
			pass
		self.y_vel = -6
		self.state = 'bumped'
		pass

	def bumped(self):
		self.rect.y += self.y_vel
		self.y_vel += self.gravity
		self.frame_index = 3

		if self.rect.y > self.y + 10:
			self.rect.y = self.y
			self.state = 'open'

		pass

	def open(self):
		pass

	def fall(self):
		pass
