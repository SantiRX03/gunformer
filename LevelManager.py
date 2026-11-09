import pygame
import random
import math
from Platforms import Platform
from Enemy import Enemy

class LevelManager:
    def __init__(self, color_player, color_enemy):
        self.color_player = color_player
        self.color_enemy = color_enemy
        self.max_map_x = 0

        self.designs = [
            [(0, 500, 300, 50, False), (420, 400, 150, 20, True)],
            [(0, 450, 150, 50, False), (250, 380, 150, 20, True), (500, 320, 150, 20, False)],
            [(0, 500, 200, 50, False), (400, 500, 250, 50, True)],
            [(0, 500, 200, 50, False), (280, 280, 100, 20, True), (460, 500, 200, 50, False)],
            [(0, 500, 600, 30, False), (150, 380, 150, 20, True), (380, 380, 150, 20, True)],
            [(0, 320, 150, 20, True), (220, 400, 150, 20, False), (440, 480, 200, 30, True)],
            [(0, 500, 200, 50, False), (500, 500, 300, 50, True)],
            [(0, 480, 100, 20, False), (180, 380, 120, 20, True), (360, 280, 120, 20, True), (700, 480, 100, 20, False)],
            [(0, 520, 800, 30, False), (150, 360, 500, 20, True)]
        ]

    def update_scroll(self, scroll):
        self.max_map_x -= scroll

    def reset(self):
        self.max_map_x = 0

    def generate_next_block(self, platform_group, enemy_group, fase_r = 0, fase_g = 0, fase_b = 0):
        chosen_block = random.choice(self.designs)
        spawn_probability = min(0.20 + (self.max_map_x / 15000), 0.85)

        frequency = self.max_map_x / 2000

        r = int(187 + 67 * math.sin(frequency + fase_r))
        g = int(187 + 67 * math.sin(frequency + fase_g))
        b = int(187 + 67 * math.sin(frequency + fase_b))

        PLATFORM_COLOR = (r, g, b)



        for plat in chosen_block:
            x_real = self.max_map_x + plat[0]
            y_real = plat[1]
            width = plat[2]
            height = plat[3]
            enemy_present = plat[4]

            new_plat = Platform(x_real, y_real, width, height, "assests/Platforms/mainplatform/0.png", PLATFORM_COLOR)
            platform_group.add(new_plat)

            if enemy_present or (random.random() < spawn_probability):
                new_enemy = Enemy(x_real + (width // 2), y_real - 40, self.color_enemy)
                enemy_group.add(new_enemy)
                if self.max_map_x > 5000:
                    new_enemy.shoot_cooldown -= 1
                    new_enemy.speed += 1
                    new_enemy.health += 1
        self.max_map_x += 800

    def clean_old_sprites(self, platform_group, enemy_group):
        for plat in platform_group:
            if plat.rect.right < 0:
                plat.kill()

        for enemy in enemy_group:
            if enemy.rect.right < 0:
                enemy.kill()



