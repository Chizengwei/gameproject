import pygame

C_GROUND_HEIGHT = 240

# R G B
black = (1, 1, 1)


def get_image(path):
	img = pygame.image.load(path)
	return img
	pass


def get_surface(surface, x, y, width, height, colorKey, scale):
	img = pygame.Surface((width, height))
	img.blit(surface, (0, 0), pygame.Rect(x, y, width, height))
	img.set_colorkey(colorKey)
	img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
	return img


def get_sounds(path):
	sound = pygame.mixer.Sound(path)
	return sound


def get_backgroundMusic(path):
	backSound = pygame.mixer.music.load(path)
	return backSound


tuples = (400, 268)
pygame.init()

# @test设置背景音乐
# get_backgroundMusic('music/happy.wav')

# 加载游戏图标图像
icon = get_image('icon/Mario1.PNG')

# 定义游戏图标
icon = pygame.transform.scale(icon, (60, 60))
iconSurface = pygame.Surface((60, 60))
icon.blit(icon, (0, 0))

# 设置声音文件字典
# sounds_dir={'death':get_sounds('music/death.wav')}

# DEATH_SOUND=sounds_dir['death']
# 获取surface

pygame.display.set_caption('SUPER MARIO')
pygame.display.set_icon(icon)
SCREEN = pygame.display.set_mode(tuples)
