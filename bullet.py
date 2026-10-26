import pygame
import math
#I fucking hate tutorial hell
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        #draws the bullet
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 223, 0))

        # rotates the bullet
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 15
        rad = math.radians(angle)
        self.dx = math.cos(rad) * self.speed
        self.dy = math.sin(rad) * self.speed

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1500


    def update(self):
        #bullet movement
        self.rect.x += self.dx
        self.rect.y += self.dy

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    