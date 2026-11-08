import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = random.randint(2, 5)
        self.image = pygame.Surface((self.size, self.size))

        self.image.fill((255, random.randint(150, 220), 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-5, 1)

        self.lifetime = random.randint(15, 30)


    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # efecto de gravedad
        self.velocity_y += 0.2 

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()