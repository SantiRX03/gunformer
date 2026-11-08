import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path = None, color =None):
        super().__init__()

        if image_path:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (width, height))

        
            if color:
                tint_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                tint_surface.fill(color)
                self.image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color if color else (0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
