import pygame


class SettingsMenu:
    def __init__(self, screen_width, screen_height, player_color, enemy_color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_color = player_color
        self.enemy_color = enemy_color

        self.font_title = pygame.font.SysFont("Arial", 50, bold = True)
        self.font_menu = pygame.font.SysFont("Arial", 30, bold = True)

        self.fullscreen = False
        self.volume = 0.5

        self.btn_fullscreen_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 80, 300, 45)
        self.btn_vol_down_rect = pygame.Rect(screen_width // 2 - 170, screen_height // 2, 50, 45)
        self.btn_vol_up_rect = pygame.Rect(screen_width // 2 + 100, screen_height // 2, 50, 45)
        self.btn_back_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 100, 160, 45)

    def draw(self, screen):
        screen.fill((10, 10, 15))
        mouse_pos = pygame.mouse.get_pos()

        txt_title = self.font_title.render("CONFIGURATION", True, self.enemy_color)
        screen.blit(txt_title, (self.screen_width // 2 - txt_title.get_width() // 2, self.screen_height // 2 - 180))

        text_fs = f"FULLSCREEN:     {'Yes' if self.fullscreen else 'No'}"
        color_fs = self.player_color if self.btn_fullscreen_rect.collidepoint(mouse_pos) else (255, 255, 255)
        txt_fs = self.font_menu.render(text_fs, True, color_fs)
        screen.blit(txt_fs, (self.screen_width // 2 - txt_fs.get_width() // 2, self.screen_height // 2 - 70))

        txt_vol_label = self.font_menu.render(f"VOLUME: {int(self.volume * 100)}%", True,(255, 255, 255))
        screen.blit(txt_vol_label, (self.screen_width // 2 - txt_vol_label.get_width() // 2, self.screen_height // 2 + 5))

        color_down = self.player_color if self.btn_vol_down_rect.collidepoint(mouse_pos) else (255, 255, 255)
        txt_down = self.font_menu.render("[-]", True, color_down)
        screen.blit(txt_down, (self.btn_vol_down_rect.x + 10, self.btn_vol_down_rect.y))

        color_up = self.player_color if self.btn_vol_up_rect.collidepoint(mouse_pos) else (255, 255, 255)
        txt_up = self.font_menu.render("[+]", True, color_up)
        screen.blit(txt_up, (self.btn_vol_up_rect.x + 10, self.btn_vol_up_rect.y))

        color_back = self.player_color if self.btn_back_rect.collidepoint(mouse_pos) else (255, 255, 255)
        txt_back = self.font_menu.render("BACK", True, color_back)
        screen.blit(txt_back, (self.screen_width // 2 - txt_back.get_width() // 2, self.screen_height // 2 + 110))

    def check_click(self, mouse_pos, screen_obj):
        if self.btn_fullscreen_rect.collidepoint(mouse_pos):
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN | pygame.SCALED)
            else:
                pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED)
        elif self.btn_vol_down_rect.collidepoint(mouse_pos):
            self.volume = max(0.0, self.volume - 0.1)
            pygame.mixer.music.set_volume(self.volume)
        elif self.btn_vol_up_rect.collidepoint(mouse_pos):
            self.volume = max(0.0, self.volume + 0.1)
            pygame.mixer.music.set_volume(self.volume)
        elif self.btn_back_rect.collidepoint(mouse_pos):
            return "back"

        return None
