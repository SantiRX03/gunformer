import pygame
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0,)) #Red
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.max_health = 100
        self.health = 100

    def draw_health_bar(self, screen):
        if self.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 40, 5))
            health_width = int(40 * (self.health / self.max_health))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5))

    def update(self):
        if self.health <= 0:
            self.kill()