# 定义游戏类
import pygame.event
import sys

from super_mario.data.main_menu import *


class Game:
    def __init__(self, state_dict, state_start):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keyDown = pygame.key.get_pressed()
        self.keyUp = pygame.key.get_pressed()
        self.event = None

        self.state_dict = state_dict
        self.state = state_dict[state_start]
        pass

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)

            if next_state == 'level':
                get_backgroundMusic('music/main_theme.ogg')
                pygame.mixer.music.play(-1, 0.0)
            elif next_state == 'game_over':
                get_backgroundMusic('music/game_over.ogg')
                pygame.mixer.music.play(-1, 0.0)
            elif next_state == 'menu':
                get_backgroundMusic('music/happy.wav')
                pygame.mixer.music.play(-1, 0.0)
            pass

        self.state.update(self.screen, self.keyDown, self.keyUp)
        self.keyUp = None
        self.keyDown = None
        pass

    def run(self):
        while True:
            pygame.display.update()
            # keys = pygame.key.get_pressed()
            for self.event in pygame.event.get():
                from pygame.constants import QUIT
                if self.event.type == QUIT:
                    pygame.quit()
                    quit()
                    sys.exit()
                    pass
                elif self.event.type == pygame.KEYDOWN:
                    self.keyDown = self.event.key
                    if self.keyDown==pygame.K_DOWN:
                        pass
                        # print(1)
                elif self.event.type == pygame.KEYUP:
                    self.keyUp = self.event.key
                    pass
                    # print(0)

            self.update()
            self.clock.tick(35)
