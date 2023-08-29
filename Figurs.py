import pygame
from pygame.locals import *
import os

pygame.init()

size = Width, hieght = 800, 450
Game = pygame.display.set_mode(size)
pygame.display.set_caption("Home-coming")
shoot = False
moving_left = False
moving_right = False
bullet = pygame.image.load("Images/Player/bullet.png").convert_alpha()
gun = pygame.image.load("Images/Player/full pistol.png").convert_alpha()
clock = pygame.time.Clock()
FPS = 60
GGravity = 0.75
BG = (144, 201, 120)
red = (255, 0, 0)


def draw_bg():
    Game.fill(BG)
    pygame.draw.line(Game, red, (0, 300), (Width, 300))


class Solider(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.health = 100
        self.max_health = self.health
        self.scale = scale
        self.start_ammo = self.ammo
        self.shootcooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True
        self.animations = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animation_type = ["idle", "Run", "Jump"]
        temp_list = []

        for animation in animation_type:
            temp_list = []
            num_of_frames = len(os.listdir(f"Images/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"Images/{self.char_type}/{animation}/pixil-frame-0 ({i}).png").convert_alpha()
                self.image = pygame.transform.scale(img, (
                int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(img)
            self.animations.append(temp_list)
        temp_list = []
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        if self.shootcooldown > 0:
            self.shootcooldown -= 1

    def update_animation(self):
        Animation_cooldown = 100
        self.image = self.animations[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > Animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animations[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(1)

    def moving(self, moving_right, moving_left):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if player.jump == True and player.in_air == False:
            self.vel_y = -11
            player.jump = False
            player.in_air = True

        self.vel_y += GGravity

        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        bbb = 300 - self.image.get_height()

        if self.rect.y + dy > bbb:
            dy = bbb - self.rect.y
            player.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        Game.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def shoot(self):
        if self.shootcooldown == 0 and self.ammo > 0:
            self.shootcooldown = 20
            bulllet = Bullet(self.rect.centerx + (50 * self.direction), self.rect.centery + -20, player.direction, bullet, 2)
            bullet_group.add(bulllet)
            self.ammo -= 1



class Create_Object(pygame.sprite.Sprite):
    def __init__(self, position, direction, object, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = object
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.direction = direction

    def draw(self, direction):
        Game.blit(pygame.transform.flip(self.image, direction, False), self.rect)

    def update(self, position, direction):
        Game.blit(pygame.transform.flip(self.image, direction, False), position)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet, scale1):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet
        self.image = pygame.transform.scale(self.image, (
        int(self.image.get_width() * scale1), int(self.image.get_height() * scale1)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > Width - 100:
            self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                print(f"player = {player.health}")
                self.kill()


        if pygame.sprite.spritecollide(Enemy, bullet_group, False):
            if player.alive:
                Enemy.health -= 25
                print(f"enemy = {Enemy.health}")
                self.kill()



bullet_group = pygame.sprite.Group()

x = 200
y = 200
scale = 0.25

player = Solider(x, y, "Player", scale, 5, 200)
gun = Create_Object(player.rect.center, player.direction, gun, 1.5)
Enemy = Solider(x, 225, "Enemyred", 0, 5, 5)

edame = True

while edame:
    draw_bg()
    clock.tick(FPS)
    player.update()
    player.draw()
    Enemy.draw()
    player.moving(moving_right, moving_left)
    bullet_group.update()
    bullet_group.draw(Game)
    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)
            gun.update((player.rect.x + 17, player.rect.y + 40), player.flip)
        elif moving_left or moving_right:
            player.update_action(1)

        else:
            player.update_action(0)
            if player.flip:
                gun.update((player.rect.x + 20, player.rect.y + 48), player.flip)
            if not player.flip:
                gun.update((player.rect.x + 55, player.rect.y + 48), player.flip)
        if moving_left:
          gun.update((player.rect.x + 30, player.rect.y + 47), player.flip)
        elif moving_right:
          gun.update((player.rect.x + 50, player.rect.y + 45), player.flip)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            edame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_e:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_e:
                shoot = False

    pygame.display.update()

pygame.quit()
