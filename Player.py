import pygame
import os
import math
from weapon import Glock
from bullet import Bullet

GRAVITY = 0.75
WEAPON_SIZE = 1
WEAPON_START_X = 300
WEAPON_START_Y = 300
weapon = Glock()


class MC(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        self.weapon = Glock()
        self.angle = 0
        self.weapon_x = x
        self.weapon_y = y
        self.shoot_cooldown = 150
        self.last_shot_time = 0
        self.max_ammo = 15
        self.ammo = 15
        self.is_reloading = False
        self.reload_time = 0
        self.reload_cooldown = 1500


        #load all images for the players 
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f'assests/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assests/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



    def update_animation(self):
        #update anim
        ANIMATION_COOLDOWN = 100
        #update image depend on c frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check time
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # reset anim
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check if there is a new action
        if new_action != self.action:
            self.action = new_action
            #update anim settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def player_rotation(self):
        self.mouse_cords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_cords[0] - self.weapon.hitbox_glock_rect.centerx)
        self.y_change_mouse_player = (self.mouse_cords[1] - self.weapon.hitbox_glock_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.weapon.glock_image = pygame.transform.rotate(self.weapon.base_glock_image, -self.angle)
        self.weapon.glock_rect = self.weapon.glock_image.get_rect(center = self.weapon.hitbox_glock_rect.center)

    def move(self, moving_left, moving_right, rolling):
        dx = 0
        dy = 0
        
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if rolling:
            dy = dy
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        #check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

        #moves the weapon
        self.weapon_x = self.rect.x + 64
        self.weapon_y = self.rect.y + 50
        self.weapon.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.weapon.hitbox_glock_rect.center = self.weapon.pos
        self.weapon.glock_rect.center = self.weapon.hitbox_glock_rect.center

    def shoot(self, bullet_group):
        current_time = pygame.time.get_ticks()

        if self.ammo <= 0 and not self.is_reloading:
            self.start_reload()
            return
        
        if current_time - self.last_shot_time > self.shoot_cooldown:
            new_bullet = Bullet(self.weapon.glock_rect.centerx, self.weapon.glock_rect.centery, self.angle)
            bullet_group.add(new_bullet)

            self.ammo -= 1 
            self.last_shot_time = current_time

    def start_reload(self):
        if not self.is_reloading and self.ammo < self.max_ammo:
            self.is_reloading = True 
            self.reload_time = pygame.time.get_ticks()

    def update_reload(self):
        if self.is_reloading:
            if pygame.time.get_ticks() - self.reload_time > self.reload_cooldwon:
                self.ammo = self.max_ammo
                self.is_reloading = False


    def update(self):
        self.player_rotation()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        screen.blit(self.weapon.glock_image, (self.weapon_x, self.weapon_y))
        self.update()