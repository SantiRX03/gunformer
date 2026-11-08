import pygame
import math
import random
from Player import GRAVITY

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.image.load("assests/Enemy/Idle/0.png").convert_alpha()

        tint_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        tint_surface.fill(color)
        self.image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vel_y = 0
        self.in_air = True

        self.max_health = 100
        self.health = 100

        self.enemy_type = random.choice(['melee', 'ranged'])
        self.speed = 2 if self.enemy_type == 'melee' else 0

        self.shoot_cooldown = 1500
        self.last_shot = pygame.time.get_ticks()

    def draw_health_bar(self, screen):
        if self.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 40, 5))
            health_width = int(40 * (self.health / self.max_health))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5))

    def update(self, player, enemy_bullet_group, platform_group):
        if self.health <= 0:
            self.kill()
            return
        dx = 0
        dy = 0

        dist_x = player.rect.centerx - self.rect.centerx
        dist_y = player.rect.centery - self.rect.centery
        distance = math.hypot(dist_x, dist_y)

        if self.enemy_type == 'melee' and distance < 300:
            if dist_x > 0:
                self.rect.x += self.speed
            elif dist_x < 0:
                self.rect.x -= self.speed

        elif self.enemy_type == 'ranged' and distance < 600:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot > self.shoot_cooldown:
                angle = math.degrees(math.atan2(dist_y, dist_x))
                projectile = EnemyBullet(self.rect.centerx, self.rect.centery, angle, (255, 0, 0))
                enemy_bullet_group.add(projectile)

                self.last_shot = current_time

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right

        self.rect.y += dy
        self.in_air = True

        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.in_air = False
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, color):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(color)
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 8
        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * self.speed
        self.velocity_y = math.sin(rad) * self.speed
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if pygame.time.get_ticks() - self.spawn_time > 2000:
            self.kill()
    