import json
import os

import pygame

from super_mario.data.powerup import Fire_ball
from super_mario.data.tools import get_image, get_surface, get_sounds


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        # 加载资源

        # 创建一个空白帧
        self.blank_img = pygame.Surface((1, 1))
        self.dead_sound = get_sounds('music/death.wav')
        self.jump_sound = get_sounds('sound/big_jump.ogg')
        self.small_jump_sound = get_sounds('sound/small_jump.ogg')
        self.load_img = get_image('graphics/mario_bros.png')

        self.frame_index = 0
        self.down_frames = []
        self.up_frames = []
        self.left_frames = []
        self.right_frames = []
        self.frames = []
        self.name = name
        self.load_date()
        self.sheet = None
        self.load_images()
        self.x_vel = 0
        self.y_vel = 0
        self.setup_timer()
        self.setup_states()
        self.setup_velocities()
        self.pressed_key = 0

    # 设置玩家状态
    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        self.can_jump = True
        self.hurt_immune = False
        self.fire = False
        self.can_shoot = False
        pass

    def load_date(self):
        file_name = self.name + '.json'
        file_path = os.path.join('dir', file_name)
        with open(file_path) as f:
            self.player_date = json.load(f)
        pass

    def die(self):
        self.rect.y += self.y_vel
        self.y_vel += self._gravity_g
        pass

    def go_die(self):
        pygame.mixer.music.stop()
        self.dead_sound.play()
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6
        self.state = 'death'
        self.death_timer = self.current_time
        pass

    def setup_velocities(self):
        speed = self.player_date['speed']
        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = 1
        self._gravity_g = 0.4

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel
        pass

    # 设置计时器初始時間
    def setup_timer(self):
        self.walking_timer = 0
        self.transition_timer = 0
        self.death_timer = 0
        self.hurt_immune_timer = 0
        self.shoot_timer = 0
        pass

    def load_images(self):
        frame_rects = self.player_date['image_frames']

        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]

        self.all_frames = [self.right_small_normal_frames,
                           self.right_big_normal_frames,
                           self.right_big_fire_frames,
                           self.left_small_normal_frames,
                           self.left_big_normal_frames,
                           self.left_big_fire_frames]

        self.right_frames = self.right_small_normal_frames
        # self.right_frames = self.left_big_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_img = get_surface(self.load_img, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                        frame_rect['height'], (0, 0, 0), 1.2)
                left_img = pygame.transform.flip(right_img, True, False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_img)
                    self.left_small_normal_frames.append(left_img)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_img)
                    self.left_big_normal_frames.append(left_img)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_img)
                    self.left_big_fire_frames.append(left_img)

        # self.right_frames.append(right_img)
        # self.left_frames.append(left_img)
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        pass

    # 更新游戏
    def update(self, keys, keyUp, surface, level):
        # if self.x_vel == 0 and self.y_vel == 0:
        #     self.state = 'stand'

        self.current_time = pygame.time.get_ticks()
        self.handle_state(keys, keyUp, level)
        self.is_hurt_immune()
        if self.state == 'jump':
            self.frame_index = 5
        elif self.hurt_immune and (self.current_time - self.hurt_immune_timer) % 100 < 50:
            self.image = self.blank_img
        else:
            self.image = self.frames[self.frame_index]
        surface.blit(self.image, self.rect)
        pass

    # 状态机
    def handle_state(self, keys, keyUp, level):
        self.can_jump_or_not(keys)
        self.can_shoot_or_not(keys)

        if self.state == 'stand':
            self.stand(keys, keyUp)
            pass
        elif self.state == 'walk':
            self.walk(keys, keyUp)
            pass
        elif self.state == 'jump':
            self.jump(keys)
            pass

        elif self.state == 'crouch':
            self.crouch(keys, keyUp)
            pass
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'death':
            self.die()

        elif self.state == 'transfiguration':
            self.transform(keys)

        elif self.state == 'big_to_small':
            self.fire = False
            self.big_to_small()

        elif self.state == 'big_to_fire':
            self.big_to_fire()

        if self.fire:
            if keys[pygame.K_a] and self.can_shoot:
                self.shoot(level)

        if self.face_right == True:
            self.frames = self.right_frames
        else:
            self.frames = self.left_frames
        pass

    def stand(self, keys, keyUp):
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys:
            print('站立狀態按鍵按下！！')
            if keys == pygame.K_LEFT:
                self.pressed_key = 0
                self.face_right = False
                self.state = 'walk'
                pass
            elif keys == pygame.K_RIGHT:
                self.pressed_key = 1
                self.face_right = True
                self.state = 'walk'
            elif keys == pygame.K_SPACE and self.can_jump:
                self.pressed_key = 2
                self.frame_index = 4
                self.state = 'jump'
                self.y_vel += self.jump_vel
            elif keys == pygame.K_DOWN and self.big:
                self.pressed_key = 3
                self.state = 'crouch'
                self.rect.y -= 10
        if keyUp:
            print('站立状态按键松开！')

    # 	下蹲状态触发

    def can_jump_or_not(self, keys):
        if not keys == pygame.K_SPACE:
            self.can_jump = True
        pass

    def walk(self, keys, keyUp):

        # 行走动画播放
        if self.current_time - self.walking_timer > self.calc_frame_duration():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
            pass
        if self.face_right:
            # self.x_vel += self.x_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_walk_vel, True)
        else:
            # self.x_vel -= self.x_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_walk_vel, False)

        if keyUp:
            # if keyUp == pygame.K_LEFT or keyUp == pygame.K_RIGHT:
            self.state = 'stand'

    def jump(self, keys):
        # self.jump_sound.play()

        self.can_jump = False
        self.frame_index = 4
        self.y_vel += self._gravity_g * 2
        if keys:
            if keys == pygame.K_LEFT:
                self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
            elif keys == pygame.K_RIGHT:
                self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        if self.y_vel > 0:
            self.state = 'fall'

    # if not keys[pygame.K_SPACE]:
    # 	self.state = 'fall'
    # pass

    def fall(self, keys):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity * .8, self.max_y_vel)
        # # TODO workaround will move
        # if self.rect.bottom > C_GROUND_HEIGHT:
        # 	self.rect.bottom = C_GROUND_HEIGHT
        # 	self.y_vel = 0
        # 	self.state = 'walk'
        if keys:
            if keys == pygame.K_LEFT:
                self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
            if keys == pygame.K_RIGHT:
                self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        pass

    # 发射火球
    def shoot(self, level):
        if self.current_time - self.shoot_timer > 200:
            self.frame_index = 6
            fireball = Fire_ball(self.rect.centerx, self.rect.centery, self.face_right)
            level.powerup_group.add(fireball)
            self.can_shoot = False
            self.shoot_timer = self.current_time
        pass

    def calc_vel(self, vel, accel, max_vel, is_positive=True):
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)
        pass

    def calc_frame_duration(self):
        duration = 200 / self.max_run_vel * abs(self.x_vel) + 30
        return duration

    def transform(self, keys):
        frame_dur = 70
        sizes = [1, 0, 1, 0, 1, 2, 0, 1, 2, 0, 2]
        frames_and_idx = [(self.small_normal_frames, 0), (self.small_normal_frames, 7), (self.big_normal_frames, 0)]

        if self.transition_timer == 0:
            self.big = True
            self.transition_timer = self.current_time
            self.changing_idx = 0
        elif self.current_time - self.transition_timer > frame_dur:
            self.transition_timer = self.current_time
            frames, idx = frames_and_idx[sizes[self.changing_idx]]
            self.change_player_image(frames, idx)
            self.changing_idx += 1
            if self.changing_idx == len(sizes):
                self.transition_timer = 0
                self.right_frames = self.right_big_normal_frames
                self.left_frames = self.left_big_normal_frames
                self.state = 'walk'
        pass

    def change_player_image(self, frames, idx):
        self.frame_index = idx
        if self.face_right:
            self.right_frames = frames[0]
            self.image = self.right_frames[self.frame_index]
        else:
            self.left_frames = frames[1]
            self.image = self.left_frames[self.frame_index]

        last_frame_bottom = self.rect.bottom
        last_frame_centerx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = last_frame_bottom
        self.rect.centerx = last_frame_centerx
        pass

    def big_to_small(self):
        frame_dur = 70
        sizes = [2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        frames_and_idx = [(self.small_normal_frames, 8), (self.big_normal_frames, 8), (self.big_normal_frames, 4)]

        if self.transition_timer == 0:
            self.big = False
            self.transition_timer = self.current_time
            self.changing_idx = 0
        elif self.current_time - self.transition_timer > frame_dur:
            self.transition_timer = self.current_time
            frames, idx = frames_and_idx[sizes[self.changing_idx]]
            self.change_player_image(frames, idx)
            self.changing_idx += 1
            if self.changing_idx == len(sizes):
                self.transition_timer = 0
                self.right_frames = self.right_small_normal_frames
                self.left_frames = self.left_small_normal_frames
                self.state = 'walk'
        pass

    def is_hurt_immune(self):
        if self.hurt_immune:
            if self.hurt_immune_timer == 0:
                self.hurt_immune_timer = self.current_time
            elif self.current_time - self.hurt_immune_timer > 2000:
                self.hurt_immune = False
                self.hurt_immune_timer = 0

    def big_to_fire(self):
        frame_dur = 70
        sizes = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        frames_and_idx = [(self.fire_frames, 3), (self.big_normal_frames, 3)]

        if self.transition_timer == 0:
            self.fire = True
            self.transition_timer = self.current_time
            self.changing_idx = 0
        elif self.current_time - self.transition_timer > frame_dur:
            self.transition_timer = self.current_time
            frames, idx = frames_and_idx[sizes[self.changing_idx]]
            self.change_player_image(frames, idx)
            self.changing_idx += 1
            if self.changing_idx == len(sizes):
                self.transition_timer = 0
                self.right_frames = self.right_big_fire_frames
                self.left_frames = self.left_big_fire_frames
                self.state = 'walk'
        pass

    def can_shoot_or_not(self, keys):
        if not keys == pygame.K_a:
            self.can_shoot = True
        pass

    def crouch(self, keys, keyUp):
        self.frame_index = 7
        if keyUp == pygame.K_DOWN:
            self.state = 'walk'
        # if keys[pygame.K_DOWN]:
        # 	self.state = 'stand'
        # 	print('up')
        pass
