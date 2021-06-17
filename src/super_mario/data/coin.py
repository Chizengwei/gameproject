import pygame


class FlashCoin(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.current_time = pygame.time.get_ticks()
		self.frames = []
		self.frame_index = 0
		frame_rects = [(1, 160, 5, 8), (9, 160, 5, 8), (17, 160, 5, 8), (160, 160, 5, 8)]
		self.load_frames(frame_rects)
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = 142
		self.rect.y = 27
		self.timer = 0
		pass

	def load_frames(self, frame_rects):
		from super_mario.data.tools import get_surface
		# sheet = get_image('graphics/item_objects.png')
		sheet = pygame.image.load('graphics/item_objects.png')
		for frame_rect in frame_rects:
			self.frames.append(get_surface(sheet, *frame_rect, (0, 0, 0), 1.5))

	def update(self):
		self.current_time = pygame.time.get_ticks()
		frame_durations = [375, 125, 125, 125]
		count = self.current_time - self.timer
		# print(count)
		if self.timer == 0:
			self.timer = self.current_time
		elif count > frame_durations[self.frame_index]:
			self.frame_index += 1
			# if self.frame_index==3:
			# 	self.frame_index=0
			self.frame_index %= 4
			self.timer = self.current_time

		self.image = self.frames[self.frame_index]
