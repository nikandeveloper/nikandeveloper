import pygame
import Figurstest as ft
import Datas

# Initialize pygame
pygame.init()

# Initialize variables
shoot = False
timerr = 100
moving_left = False
moving_right = False
tir = False
gun2 = pygame.image.load("Images/Player/full pistol.png").convert_alpha()
tir_thrown = False
edame = Datas.edamee
player_x = 200
player_y = 200
mer = False
mel = False
d = 1

# Initialize player and enemy
player3 = ft.player3
camera = ft.Camera(ft.Width, ft.hieght)

def handle_input(event):
    global moving_left, moving_right, shoot, tir, tir_thrown, d
    if event.type == pygame.QUIT:
        return False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            if not player3.alive and ft.player.alive:
                player3.alive = True
        if event.key == pygame.K_a:
            moving_left = True
            d = 1
        if event.key == pygame.K_d:
            moving_right = True
            d = 0
        if event.key == pygame.K_SPACE:
            shoot = True
        if event.key == pygame.K_LSHIFT:
            tir = True
            tir_thrown = False
        if event.key == pygame.K_w and ft.player.alive and not ft.player.in_air:
            ft.player.jump = True
        if event.key == pygame.K_c:  # Add this line to toggle camera_follow
            ft.player.camera_follow = not ft.player.camera_follow
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            moving_left = False
            d = 1
        if event.key == pygame.K_d:
            moving_right = False
            d = 0
        if event.key == pygame.K_SPACE:
            shoot = False
        if event.key == pygame.K_LSHIFT:
            tir_thrown = True
            tir = False
    return True

while edame:
    prev_player_pos = ft.player.rect.copy()

    ft.draw_bg()
    ft.clock.tick(ft.FPS)

    if moving_right and moving_left:
        mel = False
        mer = False
    elif moving_left:
        mel = True
        mer = False
    elif moving_right:
        mel = False
        mer = True
    else:
        mel = False
        mer = False
        ft.Enemy.update_action(0)

    if ft.player.alive:
        ft.player.update()
        ft.player.moving(moving_right, moving_left)
        if ft.player.camera_follow:  # Update camera only if camera_follow is True
            camera.update(ft.player)

    if ft.player.alive:
        if shoot:
            ft.player.shoot()
        elif tir and not tir_thrown and ft.player.tiran > 0:
            tirzadan = ft.tirc(ft.player.rect.centerx + (1 * ft.player.rect.size[0] * ft.player.direction),
                               ft.player.rect.top - 20,
                               ft.player.direction, ft.nize_hormazdgan, 2, 100)
            ft.tir_mazda_group.add(tirzadan)
            tir_thrown = True
            ft.player.tiran -= 1
        if ft.player.in_air:
            ft.player.update_action(2)
        elif not moving_left and not moving_right:
            ft.player.update_action(0)
        elif moving_left or moving_right:
            ft.player.update_action(1)

    if ft.Enemy.alive:
        ft.Enemy.update()
        ft.Enemy.moving(mer, mel)
    else:
        ft.Enemy.dead()

    if ft.player.alive:
        if ft.player.rect.y < 241:
            ft.player.in_air = True
        else:
            ft.player.in_air = False

    if ft.Enemy.alive:
        if ft.player.rect.colliderect(ft.Enemy.rect):
            if prev_player_pos.bottom <= ft.Enemy.rect.top < ft.player.rect.bottom:
                ft.player.rect.bottom = ft.Enemy.rect.top
            elif prev_player_pos.top >= ft.Enemy.rect.bottom > ft.player.rect.top:
                ft.player.rect.top = ft.Enemy.rect.bottom
            elif prev_player_pos.right <= ft.Enemy.rect.left < ft.player.rect.right:
                ft.player.rect.right = ft.Enemy.rect.left
            elif prev_player_pos.left >= ft.Enemy.rect.right > ft.player.rect.left:
                ft.player.rect.left = ft.Enemy.rect.right

    if player3.alive:
        player3.update((player_x, player_y), d)

    ft.gun.update((ft.player.rect.x + 6, ft.player.rect.y + 27), ft.player.flip)

    ft.statics_group.draw(ft.Game)
    ft.statics_group.update()
    ft.bullet_group.update()
    ft.bullet_group.draw(ft.Game)
    ft.tir_mazda_group.update()
    ft.tir_mazda_group.draw(ft.Game)
    ft.gun_group.update()
    ft.gun_group.draw(ft.Game)
    ft.explosion_group.update()
    ft.explosion_group.draw(ft.Game)
    timerr -= 0.01

    for event in pygame.event.get():
        if not handle_input(event):
            edame = False

    pygame.display.update()

pygame.quit()
