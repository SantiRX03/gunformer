import pygame
WEAPON_SIZE = 1
WEAPON_START_X = 300
WEAPON_START_Y = 300

class Glock:
    def __init__(self):
        self.pos = pygame.math.Vector2(WEAPON_START_X, WEAPON_START_Y)
        self.glock_image = pygame.transform.rotozoom(pygame.image.load("assests/Weapon/Glock/glock.png"), 0, WEAPON_SIZE)
        self.base_glock_image = self.glock_image
        self.hitbox_glock_rect = self.base_glock_image.get_rect(center = self.pos)
        self.glock_rect = self.hitbox_glock_rect.copy()

        self.image = self.glock_image
        self.base_image = self.base_glock_image
        self.hitbox_rect = self.hitbox_glock_rect
        self.rect = self.glock_rect

class Sniper:
    def __init__(self):
        self.pos = pygame.math.Vector2(WEAPON_START_X, WEAPON_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("assests/Weapon/Sniper/sniper.png"), 0, WEAPON_SIZE)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()

        self.glock_image = self.image
        self.base_glock_image = self.base_image
        self.hitbox_glock_rect = self.hitbox_rect
        self.glock_rect = self.rect

class Shotgun:
    def __init__(self):
        self.pos = pygame.math.Vector2(WEAPON_START_X, WEAPON_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("assests/Weapon/Shotgun/shotgun.png"), 0, WEAPON_SIZE)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()

        self.glock_image = self.image
        self.base_glock_image = self.base_image
        self.hitbox_glock_rect = self.hitbox_rect
        self.glock_rect = self.rect

class Knife:
    def __init__(self):
        self.pos = pygame.math.Vector2(WEAPON_START_X, WEAPON_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("assests/Weapon/Knife/knife.png"), 0, WEAPON_SIZE)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()

        self.glock_image = self.image
        self.base_glock_image = self.base_image
        self.hitbox_glock_rect = self.hitbox_rect
        self.glock_rect = self.rect