import pygame
import math
from Player import MC, PLAYER_COLOR
from Enemy import Enemy
from Platforms import Platform
from Particles import Particle
from LevelManager import LevelManager

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ENEMY_COLOR = (255 - PLAYER_COLOR[0], 255 - PLAYER_COLOR[1], 255 - PLAYER_COLOR[2])
# WHY THE FUCK I CHOOSE PYGAMEEEE I SHOULD STICK WITH GODOOOOOOT

pygame.init()
pygame.font.init()
scroll = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gunformer")
clock = pygame.time.Clock()
font_hud = pygame.font.SysFont("Arial", 26, bold = True)
font_gameover = pygame.font.SysFont("Arial", 50, bold = True)
font_sub = pygame.font.SysFont("Arial", 20)
score = 0
distance_traveled = 0
def reset_game():
    global player, score, distance_traveled, scroll, moving_left, moving_right, moving_right, rolling
    bullet_group.empty()
    enemy_group.empty()
    enemy_bullet_group.empty()
    particle_group.empty()
    platform_group.empty()
    score = 0
    distance_traveled = 0
    scroll = 0
    moving_left = False
    moving_right = False
    rolling = False
    level_manager.reset()
    player = MC('player', 0, 200, 3, 5, PLAYER_COLOR)
    level_manager.generate_next_block(platform_group, enemy_group)
    level_manager.generate_next_block(platform_group, enemy_group)



player = MC('player', 0, 200, 3, 5, PLAYER_COLOR)
#actions of the player
moving_left = False
moving_right = False
level_manager = LevelManager(PLAYER_COLOR, ENEMY_COLOR)

bg = (15, 15, 25)
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()


reset_game()

def draw_bg():
    screen.fill(bg)
running = True
while running:
    draw_bg()

    #update player actions
    if player.alive:
        player.update_reload()
        player.player_rotation()
        if player.in_air:
            player.update_action(2)#2 = jump
        elif moving_left or moving_right:
            player.update_action(1) #1 = run
        else:
            player.update_action(0) #0 = idle
        player.move(moving_left, moving_right, rolling, platform_group)
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
                player.shoot(bullet_group)

        if player.rect.right > SCREEN_WIDTH / 2 and moving_right:
            scroll = player.speed
            player.rect.x -= scroll
            distance_traveled += scroll // 2
            for platform in platform_group:
                platform.rect.x -= scroll
            for enemy in enemy_group:
                enemy.rect.x -= scroll
            for particle in particle_group:
                particle.rect.x -= scroll
            for bullet in bullet_group:
                bullet.rect.x -= scroll
            for e_bullet in enemy_bullet_group:
                e_bullet.rect.x -= scroll
        else:
            scroll = 0

        bullet_group.update()
        enemy_group.update(player, enemy_bullet_group, platform_group)
        enemy_bullet_group.update()

        if pygame.sprite.spritecollide(player, enemy_bullet_group, True):
            player.explode(particle_group)
        if pygame.sprite.spritecollide(player, enemy_group, False):
            player.explode(particle_group)
        if player.rect.top > 700:
            player.explode(particle_group)

        player.update_animation()
    else:
        pass

    if not player.time_stopped:
        enemy_group.update(player, enemy_bullet_group, platform_group)
        enemy_bullet_group.update()
        particle_group.update()
    else:
        pass
    if player.alive:
        for e_bullet in enemy_bullet_group:
            if player.rect.colliderect(e_bullet.rect):
                if player.check_perfect_dodge(e_bullet.rect, particle_group):
                    e_bullet.kill()
                elif not player.invulnerable:
                    player.explode(particle_group)
        for enemy in enemy_group:
            if player.rect.colliderect(enemy.rect):
                if player.check_perfect_dodge(enemy.rect, particle_group):
                    pass
                elif not player.invulnerable:
                    player.explode(particle_group)
        if player.rect.top > SCREEN_HEIGHT:
            player.explode(particle_group)

    level_manager.update_scroll(scroll)
    if level_manager.max_map_x < SCREEN_WIDTH + 200:
        level_manager.generate_next_block(platform_group, enemy_group)
    level_manager.clean_old_sprites(platform_group, enemy_group)
    


    particle_group.update()
    hits = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)
    for enemy, bullets in hits.items():
        for bullet in bullets:
            if player.current_weapon == "shotgun":
                dist = math.hypot(player.rect.centerx - enemy. rect.centerx, player.rect.centery - enemy.rect.centery)
                enemy.health -= 100 if dist < 120 else 30
            if player.current_weapon == "sniper":
                dist = math.hypot(player.rect.centerx - enemy. rect.centerx, player.rect.centery - enemy.rect.centery)
                enemy.health -= 75 + dist
            else:
                enemy.health -= 50

            if enemy.health <= 0:
                score += 100
            
            
    pygame.sprite.groupcollide(platform_group, enemy_bullet_group, False, True)
    for bullet in bullet_group:
        hit_platforms = pygame.sprite.spritecollide(bullet, platform_group, False)
        if hit_platforms:
            for _ in range(8):
                spark = Particle(bullet.rect.centerx, bullet.rect.centery)
                particle_group.add(spark)

            bullet.kill()

    pygame.sprite.groupcollide(platform_group, bullet_group, False, True)


    enemy_bullet_group.draw(screen)
    platform_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    particle_group.draw(screen)
    for enemy in enemy_group:
        enemy.draw_health_bar(screen)
    if player.alive:
        player.draw(screen)

    level_manager.update_scroll(scroll)

    if level_manager.max_map_x < SCREEN_WIDTH:
        level_manager.generate_next_block(platform_group, enemy_group)

    level_manager.clean_old_sprites(platform_group, enemy_group) 
    txt_score = font_hud.render(f"POINTS: {score}", True, (255, 255, 255))
    txt_dist = font_hud.render(f"DISTANCE: {distance_traveled}m", True, (255, 255, 255))
    txt_ammo = font_hud.render(f"AMMO: {'RELOADING. . .' if player.is_reloading else f'{player.ammo}/{player.max_ammo}'}", True, (255, 255, 255))

    screen.blit(txt_score, (20, 20))
    screen.blit(txt_score, (20, 55))
    screen.blit(txt_score, (SCREEN_WIDTH - 250, 20))


    if not player.alive:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.screen.blit(overlay, (0, 0)) if hasattr(screen, "screen") else screen.blit(overlay, (0, 0))

        txt_gameover = font_gameover.render("KABOOM!!! GAME OVER", True, ENEMY_COLOR)
        txt_restart = font_sub.render("Press ENTER to start again", True, (200, 200, 200))
        txt_final_stats = font_sub.render(f"Final Score: {score} pts | Max Distance {distance_traveled}m", True, (255, 255, 255))

        screen.blit(txt_gameover, (SCREEN_WIDTH // 2 - txt_gameover.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(txt_final_stats, (SCREEN_WIDTH // 2 - txt_final_stats.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(txt_restart, (SCREEN_WIDTH // 2 - txt_restart.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    for event in pygame.event.get():
        #QUIT
        if event.type == pygame.QUIT:
            running = False
        #keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player.alive:
                moving_left = True
            if event.key == pygame.K_d and player.alive:
                moving_right = True
            if event.key in [pygame.K_LSHIFT, pygame.K_s] and player.alive:
                player.trigger_dash()
            if event.key in [pygame.K_SPACE, pygame.K_w] and player.alive:
                player.trigger_jump()
            if event.type == pygame.MOUSEBUTTONDOWN and player.alive:
                if event.button == 1:
                    player.shoot(bullet_group)
            if event.type == pygame.K_r and player.alive:
                player.start_reload()
            if event.key == pygame.K_q and player.alive:
                player.throw_knife(bullet_group)
                player.change_weapon("glock")
            if event.key == pygame.K_1: 
                player.change_weapon("glock")
                player.current_weapon = "glock"
            if event.key == pygame.K_2: 
                player.change_weapon("sniper")
                player.current_weapon = "sniper"
                player.sniper_recomposing = False
            if event.key == pygame.K_3: 
                player.change_weapon("shotgun")
                player.current_weapon = "shotgun"
                player.weapon_uses = 5
            if event.key == pygame.K_4: 
                player.change_weapon("knife")
                player.current_weapon = "knife"
            if event.key == pygame.K_RETURN and not player.alive:
                reset_game()
            if event.key == pygame.K_ESCAPE:
                running = False
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()
    clock.tick(60)
pygame.quit()