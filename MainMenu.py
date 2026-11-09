import pygame

class MainMenu:
    def __init__(self, screen_width, screen_height, player_color, enemy_color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_color = player_color
        self.enemy_color = enemy_color

        self.font_title = pygame.font.SysFont("Arial", 65, bold = True)
        self.font_menu = pygame.font.SysFont("Arial", 35, bold = True)

        self.btn_start_rect = pygame.Rect(screen_width // 2 - 120, screen_height // 2 - 20, 240, 50)
        self.btn_settings_rect = pygame.Rect(screen_width // 2 - 120, screen_height // 2 + 10, 240, 50)
        self.btn_quit_rect = pygame.Rect(screen_width // 2 - 120, screen_height // 2 + 60, 240, 50)
    
    def draw(self, screen):
        screen.fill((10, 10, 15))

        mouse_pos = pygame.mouse.get_pos()
        txt_title = self.font_title.render("GUNFORMER", True, self.enemy_color)
        screen.blit(txt_title, (self.screen_width // 2 - txt_title.get_width() // 2, self.screen_height // 2 - 180)) 
        
        color_start = self.player_color if self.btn_start_rect.collidepoint(mouse_pos) else (255, 255, 255) 
        txt_start = self.font_menu.render("START GAME", True, color_start) 
        screen.blit(txt_start, (self.screen_width // 2 - txt_start .get_width() // 2, self.screen_height // 2 - 10)) 

        color_set = self.player_color if self.btn_settings_rect.collidepoint(mouse_pos) else (255, 255, 255)
        txt_set = self.font_menu.render("SETTINGS", True, color_set)
        screen.blit(txt_set, (self.screen_width // 2 - txt_set.get_width() // 2, self.screen_height // 2 + 40))
        
        color_quit = self.player_color  if self.btn_quit_rect.collidepoint(mouse_pos) else ( 255, 255, 255) 
        txt_quit = self.font_menu.render("QUIT", True, color_quit)
        screen.blit(txt_quit, (self.screen_width // 2 - txt_quit.get_width() // 2, self.screen_height // 2 + 90))
    
    def check_click(self, mouse_pos):
        if self.btn_start_rect.collidepoint(mouse_pos):
            return "start"
        if self.btn_settings_rect.collidepoint(mouse_pos):
            return "settings"
        if self.btn_quit_rect.collidepoint(mouse_pos):
            return "quit"
        return None
    