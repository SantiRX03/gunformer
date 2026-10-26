import pygame
from Player import MC
from Enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Gunformer")
clock = pygame.time.Clock()
player = MC('player', 200, 200, 3, 5)
#actions of the player
moving_left = False
moving_right = False
rolling = False

bg = (0, 0, 139)
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

test_enemy = Enemy(600, 260)
enemy_group.add(test_enemy)


running = True
while running:

    screen.fill(bg)
    player.update_animation()
    player.draw(screen)


    #update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)#2 = jump
        elif moving_left or moving_right:
            player.update_action(1) #1 = run
        else:
            player.update_action(0) #0 = idle
        player.move(moving_left, moving_right, rolling)

    bullet_group.update()
    bullet_group.draw(screen)
    enemy_group.update()

    hits = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)

    for enemy, bullets in hits.items():
        for bullet in bullets:
            enemy.health -= 25

    bullet_group.draw(screen)

    for enemy in enemy_group:
        enemy.draw_health_bar(screen)

    


    pygame.display.update()
    clock.tick(60)

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        player.shoot(bullet_group)
    
    for event in pygame.event.get():
        #QUIT
        if event.type == pygame.QUIT:
            running = False
        #keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_s:
                rolling = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(bullet_group)
            if event.type == pygame.K_r:
                player.start_reload()
            if event.key == pygame.K_ESCAPE:
                running = False
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s or pygame.K_LSHIFT:
                rolling = False
            if event.key == pygame.K_w or pygame.K_SPACE:
                player.jump = False
            
pygame.quit()