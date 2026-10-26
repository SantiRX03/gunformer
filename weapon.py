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