import pygame
import os
import math
import random
from Particles import Particle
from weapon import Glock, Sniper, Shotgun, Knife
from bullet import Bullet

GRAVITY = 0.75
WEAPON_SIZE = 1
WEAPON_START_X = 300
WEAPON_START_Y = 300
PLAYER_COLOR = (random.randint(120, 255), random.randint(120, 255), random.randint(120, 255))
weapon = Glock()


class MC(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, color):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        #vertical velocity
        self.vel_y = 0
        #jumping
        self.jump = False
        self.max_jump = 2
        self.jump_count = 0
        self.in_air = True
        #roll/dash
        self.is_rolling = False
        self.roll_cooldown = 600
        self.last_roll_time = 0
        self.roll_duration = 200
        self.max_dash_speed = 12
        self.invulnerable = False

        #perfect dash/parry
        self.time_stopped = False
        self.time_stop_start = 0
        self.time_stop_duration = 2000


        #animation
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        self.color = color

        self.weapon = Glock()
        self.current_weapon = "glock"
        self.weapon_uses = 0
        self.sniper_recomposing = False
        self.sniper_recompose_time = 0
        self.angle = 0
        self.weapon_x = x
        self.weapon_y = y
        self.shoot_cooldown = 300
        self.last_shot_time = 0
        self.max_ammo = 5
        self.ammo = 1
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


    def change_weapon(self, weapon_name):
        self.current_weapon = weapon_name
        if weapon_name == "glock":
            self.weapon = Glock()
            self.shoot_cooldown = 300
            self.max_ammo = 15
        if weapon_name == "sniper":
            self.weapon = Sniper()
            self.shoot_cooldown = 500
            self.max_ammo = 5
            if self.ammo > self.max_ammo:
                self.ammo = self.max_ammo
        if weapon_name == "shotgun":
            self.weapon = Shotgun()
            self.shoot_cooldown = 500
            self.weapon_uses = 5
            self.max_ammo = 5
            if self.ammo > self.max_ammo:
                self.ammo = self.max_ammo
        if weapon_name == "knife":
            self.weapon = Knife()
            self.shoot_cooldown = 200


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
        self.x_change_mouse_player = (self.mouse_cords[0] - self.weapon.hitbox_rect.centerx)
        self.y_change_mouse_player = (self.mouse_cords[1] - self.weapon.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.weapon.image = pygame.transform.rotate(self.weapon.base_image, -self.angle)
        self.weapon.rect = self.weapon.glock_image.get_rect(center = self.weapon.hitbox_rect.center)

    def move(self, moving_left, moving_right, rolling, platform_group):
        current_time = pygame.time.get_ticks()
        dx = 0
        dy = 0

        if self.is_rolling:
            if current_time - self.last_roll_time > self.roll_duration:
                self.is_rolling = False
                self.invulnerable = False
            else:
                self.invulnerable = True
                dx = self.speed * 1.7 * self.direction
                dash_velocity = min(5, self.max_dash_speed)
                dx = dash_velocity * self.direction

        if not self.is_rolling:
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -5
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 5

        if rolling and current_time - self.last_roll_time > self.roll_cooldown:
            self.is_rolling = True
            self.invulnerable = True
            self.last_roll_time = current_time

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        

        self.rect.x += dx
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right
        self.rect.y += dy

        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                #check if above platform
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.in_air = False
                    self.jump_count = 0 
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        #moves the weapon
        self.weapon_x = self.rect.x + 64
        self.weapon_y = self.rect.y + 50
        self.weapon.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.weapon.hitbox_glock_rect.center = self.weapon.pos
        self.weapon.glock_rect.center = self.weapon.hitbox_glock_rect.center

    def trigger_jump(self):
        if not self.in_air:
            self.vel_y = -16
            self.in_air = True
            self.jump_count = 1
        elif self.in_air and self.jump_count < self.max_jump:
            self.vel_y = -11
            self.jump_count += 1
            

    def trigger_dash(self):
        current_time = pygame.time.get_ticks()
        if not self.is_rolling and (current_time - self.last_roll_time > self.roll_cooldown):
            self.is_rolling = True
            self.invulnerable = True
            self.last_roll_time = current_time

    def shoot(self, bullet_group):
        current_time = pygame.time.get_ticks()
        if self.is_rolling and not self.time_stopped:
            return
        if self.sniper_recomposing:
            if current_time - self.sniper_recompose_time > 1000:
                self.sniper_recomposing = False
            else:
                if self.current_weapon == "sniper":
                    return
        if self.is_reloading:
            return
        if self.current_weapon != "knife":
            if self.ammo <= 0:
                self.start_reload()
                return
        if current_time - self.last_shot_time > self.shoot_cooldown:
            from bullet import Bullet
            self.last_shot_time = current_time
            self.player_rotation()
            if self.current_weapon == "glock":
                new_bullet = Bullet(self.weapon_x, self.weapon_y, self.angle)
                bullet_group.add(new_bullet)
                self.ammo -= 1
            elif self.current_weapon == "sniper":
                new_bullet = Bullet(self.weapon_x, self.weapon_y, self.angle)
                new_bullet.speed = 35
                bullet_group.add(new_bullet)
                self.ammo -= 1
                self.sniper_recomposing = True
                self.sniper_recompose_time = current_time
            elif self.current_weapon == "shotgun":
                for dispersion in [-10, -5, 0, 5, 10]:
                    perdigon = Bullet(self.weapon_x, self.weapon_y, self.angle + dispersion)
                    perdigon.lifetime = 400
                    bullet_group.add(perdigon)
                self.ammo -= 1
                if self.ammo <= 0:
                    self.weapon_uses -= 1
                if self.weapon_uses <= 0:
                    self.change_weapon("glock")
                if self.weapon_uses <= 0:
                    self.current_weapon = "glock"
            elif self.current_weapon == "knife":
                    cut = Bullet(self.weapon_x + (self.direction * 40), self.weapon_y, self.angle)
                    cut.image = pygame.Surface((15, 15), pygame.SRCALPHA)
                    cut.lifetime = 80
                    bullet_group.add(cut)

    def check_perfect_dodge(self, incoming_hitbox, particle_group):
        current_time = pygame.time.get_ticks()
        if self.is_rolling and (current_time - self.last_roll_time < 400) and not self.time_stopped:
            self.time_stopped = True
            self.time_stop_start = current_time
            for _ in range(25):
                spark = Particle(self.rect.centerx, self.rect.centery)
                spark.image.fill((0, 255, 255))
                spark.velocity_x *= 1.5
                spark.velocity_y *= 1.5
                particle_group.add(spark)
            return True
        return False

    def throw_knife(self, bullet_group):
        if self.current_weapon == "knife":
            from bullet import Bullet
            throw = Bullet(self.weapon_x, self.weapon_y, self.angle)
            throw.speed = 20
            bullet_group.add(throw)
            self.current_weapon = "glock"
    
    def start_reload(self):
        if not self.is_reloading and self.ammo < self.max_ammo:
            self.is_reloading = True 
            self.reload_time = pygame.time.get_ticks()

    def update_reload(self):
        if self.is_reloading:
            if pygame.time.get_ticks() - self.reload_time > self.reload_cooldown:
                self.ammo = self.max_ammo
                self.is_reloading = False

    def explode(self, particle_group):
        from Particles import Particle

        for _ in range(40):
            spark = Particle(self.rect.centerx, self.rect.centery)
            spark.image.fill(self.color)

            import random
            spark.velocity_x = random.randint(-7, 7)
            spark.velocity_y = random.randint(-7, 7)
            spark.lifetime = random.randint(30, 50)

            particle_group.add(spark)
        self.alive = False


    def update(self):
        self.player_rotation()

    def draw(self, screen):
        final_image = pygame.transform.flip(self.image, self.flip, False).copy()
        tint_surface = pygame.Surface(final_image.get_size(), pygame.SRCALPHA)
        tint_surface.fill(self.color)
        final_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(final_image, self.rect)
        screen.blit(self.weapon.image, (self.weapon_x, self.weapon_y))
        self.update()