import pygame
import Figurstest as ft
import Datas

shoot = False
timerr = 100
moving_left = False
moving_right = False
tir = False
gun2 = pygame.image.load("Images/Player/full pistol.png").convert_alpha()
tir_thrown = False
edame = True
player_x = 200
player_y = 200
d = 1

player3 = ft.player3

while edame:
    ft.draw_bg()
    ft.clock.tick(ft.FPS)

    if ft.player.alive:
        ft.player.draw()
        ft.player.update()
        ft.player.moving(moving_right, moving_left)
    if ft.Enemy.alive:
        ft.Enemy.draw()
        ft.Enemy.update()
    else:
        ft.Enemy.dead()


    if ft.player.alive:
        if shoot:
            ft.player.shoot()
        elif tir and not tir_thrown and ft.player.tiran > 0:
            tirzadan = ft.tirc(ft.player.rect.centerx + (1 * ft.player.rect.size[0] * ft.player.direction),
                               ft.player.rect.top - 20,
                               ft.player.direction, ft.nize_hormazdgam, 2, 100)
            ft.tir_mazda_group.add(tirzadan)
            tir_thrown = True
            tirzadan.update()
            ft.player.tiran -= 1
        if ft.player.in_air:
            ft.player.update_action(2)
        elif not moving_left and not moving_right:
            ft.player.update_action(0)
        elif moving_left or moving_right:
            ft.player.update_action(1)
        if ft.player.flip:
            ft.gun.update((ft.player.rect.x, ft.player.rect.y + 27), ft.player.flip)
        elif not ft.player.flip:
            ft.gun.update((ft.player.rect.x + 10, ft.player.rect.y + 27), ft.player.flip)

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

    if player3.alive:
        player3.update((player_x, player_y), d)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            edame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if not player3.alive:
                    if ft.player.alive:
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
            if event.key == pygame.K_w and ft.player.alive:
                ft.player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                player_x -= 20
                d = 1
            if event.key == pygame.K_d:
                moving_right = False
                player_x += 20
                d = 0
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_LSHIFT:
                tir_thrown = True
                tir = False

    pygame.display.update()

pygame.quit()
