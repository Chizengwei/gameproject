import super_mario.data.powerup
from super_mario.data import powerup
from super_mario.data.tools import *

GRAVITY = 5


class Brick(pygame.sprite.Sprite):

	def __init__(self, x, y, brick_type, group, color=0, name='brick'):
		pygame.sprite.Sprite.__init__(self)
		self.gravity = GRAVITY
		self.group = group
		self.state = 'rest'
		self.img = get_image('graphics/tile_set.png')
		self.x = x
		self.y = y
		self.brick_type = brick_type
		bright_rect_frames = [(16, 0, 16, 16), (48, 0, 16, 16)]
		dark_rect_frames = [(16, 32, 16, 16), (48, 32, 16, 16)]

		if not color:
			self.frame_rects = bright_rect_frames
		else:
			self.frame_rects = dark_rect_frames

		self.frames = []
		for frame_rect in self.frame_rects:
			self.frames.append(get_surface(self.img, *frame_rect, (0, 0, 0), 1.25))
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		self.name = name

	def update(self):
		self.handle_state()
		pass

	pass

	def handle_state(self):
		if self.state == 'rest':
			self.rest()
		if self.state == 'bumped':
			self.bumped()
		pass

	def rest(self):
		pass

	def go_bump(self):
		self.y_vel = -6
		self.state = 'bumped'
		pass

	def bumped(self):
		self.rect.y += self.y_vel
		self.y_vel += self.gravity

		if self.rect.y > self.y + 5:
			self.rect.y = self.y
			if self.brick_type == 0:
				self.state = 'rest'
			elif self.brick_type == 1:
				self.state = 'open'
			else:
				self.group.add(powerup.create_powerup(self.rect.centerx, self.rect.centery, self.brick_type))

	def open(self):
		self.frame_index = 1
		self.image = self.frames[self.frame_index]
		pass

	def smashed(self, group):
		debris = [
			(self.rect.x, self.rect.y, -2, -10),
			(self.rect.x, self.rect.y, 2, -10),
			(self.rect.x, self.rect.y, -2, -5),
			(self.rect.x, self.rect.y, 2, -5)
		]
		for d in debris:
			group.add(Debris(*d))
		self.kill()


class Debris(pygame.sprite.Sprite):

	def __init__(self, x, y, x_vel, y_vel):
		pygame.sprite.Sprite.__init__(self)
		self.img = get_image('graphics/tile_set.png')
		self.image = get_surface(self.img, 68, 20, 8, 8, (0, 0, 0), 1.2)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.gravity = GRAVITY

	# *args可变参数
	def update(self, *args):
		self.rect.x += self.x_vel
		self.rect.y += self.y_vel
		self.y_vel += self.gravity

		if self.rect.y > SCREEN.get_width():
			self.kill()
		pass
