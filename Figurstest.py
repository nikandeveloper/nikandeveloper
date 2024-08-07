import pygame
from pygame.locals import *
import os
import time
import Datas

pygame.init()
pygame.mixer.init()

size = Width, height = 800, 450
Game = pygame.display.set_mode(size)
pygame.display.set_caption("Home-coming")

bullet = pygame.image.load("Images/Player/bullet.png").convert_alpha()
gun = pygame.image.load("Images/Player/full pistol.png").convert_alpha()
nize_hormazdgam = pygame.image.load("Images/Player/nize hormazdgan.png").convert_alpha()
seda = pygame.mixer.Sound("SSKHZ9.mp3")
seda1w = pygame.mixer.Sound("war_horn_3.mp3")
pygame.transform.scale(gun, (gun.get_width() * 5, gun.get_height() * 5))
clock = pygame.time.Clock()
FPS = 60
GGravity = 0.75
BG = (144, 201, 120)
red = (255, 0, 0)
timerr1 = int(seda1w.get_length())
playtir = False


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)

        # Limit scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - target.rect.width), x)
        y = max(-(self.height - target.rect.height), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)

camera = Camera(2000, Width)


def draw_bg():
    Game.fill(BG)
    pygame.draw.line(Game, red, (0, 300), (Width, 300))


class Solider(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type, scale, killwhenfinish, speed, ammo, tiran, animationfinish, camera_follow):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.animationfinish = animationfinish
        self.killwhenfinish = killwhenfinish
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.tiran = tiran
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
        self.animation_type = ["idle", "Run", "Jump", "Death"]
        temp_list = []
        if not self.alive:
            Solider.kill()
        for animation in self.animation_type:
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
        self.camera_follow = camera_follow

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shootcooldown > 0:
            self.shootcooldown -= 1

    def dead(self):
        ...

    def update_animation(self):
        Animation_cooldown = 100
        self.image = self.animations[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > Animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animations[self.action]):
            self.animationfinish = 1
            if self.action == 3:
                self.frame_index = len(self.animations[self.action]) - 1
            else:
                self.frame_index = 0

            if self.killwhenfinish:
                self.kill()

            return self.animationfinish

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.update_action(3)
            time.sleep(0.25)
            self.alive = False

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
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GGravity

        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        bbb = 300 - self.image.get_height()

        if self.rect.y + dy > bbb:
            dy = bbb - self.rect.y
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, camera):
        if self.camera_follow:
            Game.blit(pygame.transform.flip(self.image, self.flip, False), camera.apply(self))
        else:
            Game.blit(pygame.transform.flip(self.image, self.flip, False), self.rect.topleft)

    def shoot(self):
        if self.shootcooldown == 0 and self.ammo > 0:
            self.shootcooldown = 20
            bulllet = Bullet(self.rect.centerx + (25 * self.direction), self.rect.centery + 3, self.direction, bullet,
                             2, 20)
            bullet_group.add(bulllet)
            self.ammo -= 1


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, notloop, endmethode, killwhenfinish, Animation_coooldown, chartype, nameoffolder,
                 animationfinish):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = chartype
        self.animationfinish = animationfinish
        self.scale = scale
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.notlooop = notloop
        self.jump = False
        self.in_air = True
        self.animations = []
        self.frame_index = 0
        self.action = 0
        self.timme = Animation_coooldown
        self.killwhenfinish = killwhenfinish
        self.update_time = pygame.time.get_ticks()
        self.animation_type = [nameoffolder]
        temp_list = []
        for animation in self.animation_type:
            temp_list = []
            num_of_frames = len(os.listdir(f"Images/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"Images/{self.char_type}/{animation}/pixil-frame-0 ({i}).png").convert_alpha()
                self.image = pygame.transform.scale(img, (
                    int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(self.image)
            self.animations.append(temp_list)
        temp_list = []
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if self.frame_index >= len(self.animations[self.action]):
            endmethode()

    def update(self):
        Animation_cooldown = 100
        self.image = self.animations[self.action][self.frame_index]
        if (pygame.time.get_ticks() * self.timme) - self.update_time > Animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            print(self.frame_index)

        if self.frame_index >= len(self.animations[self.action]):
            self.animationfinish = 1
            if not self.notlooop:
                self.frame_index = 0
                print("fffffff")
            else:
                self.frame_index = len(self.animations[self.action]) - 1
            if self.killwhenfinish:
                self.kill()
                print("eeeeeeee")

            return self.animationfinish


class Create_Object(pygame.sprite.Sprite):
    def __init__(self, position, object, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = object
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.alive = True

    def draw(self, direction):
        Game.blit(pygame.transform.flip(self.image, direction, False), camera.apply(self))

    def update(self, position, direction):
        Game.blit(pygame.transform.flip(self.image, direction, False), camera.apply(self))

    def death(self):
        self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet, scale1, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = bullet
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale1), int(self.image.get_height() * scale1)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def draw(self):
        Game.blit(pygame.transform.flip(self.image, self.direction, False), camera.apply(self))

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > Width - 100:
            self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
                print(f"player = {player.health}")
                if player.health == 0:
                    player.animations = 1

        if pygame.sprite.spritecollide(Enemy, bullet_group, False):
            if player.alive:
                if Enemy.alive:
                    Enemy.health -= 25
                    self.kill()
                    print(f"enemy = {Enemy.health}")
                    if Enemy.health == 0:
                        Enemy.alive = False


class tirc(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, tiir, scale1, timer):
        pygame.sprite.Sprite.__init__(self)
        self.timer = timer
        self.vel_y = -2
        self.speed = 20
        self.image = tiir
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale1), int(self.image.get_height() * scale1)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += (GGravity / 4)
        dx = self.direction * self.speed
        dy = self.vel_y

        if self.rect.left + dx < 0 or self.rect.right + dx > Width - 100:
            self.direction *= -1
            dx = self.direction * self.speed
            pygame.mixer.Sound.play(seda1w)
            explosion = Object(self.rect.x + 57, self.rect.y - 183, 5, True, self.dprint(), True, 0.75, "particles",
                               "Explosion", 0)
            explosion_group.add(explosion)

        if pygame.sprite.spritecollide(player, tir_mazda_group, False):
            if player.alive:
                player.health -= 100
                print(f"player = {player.health}")

        bbb = 300 - self.image.get_height()
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0
            pygame.mixer.Sound.play(seda1w)
            explosion = Object(self.rect.x + 57, self.rect.y - 180, 5, True, self.dprint(), True, 0.75, "particles",
                               "Explosion", 0)
            explosion_group.add(explosion)
            self.kill()

        if pygame.sprite.spritecollide(player, explosion_group, False):
            if player.alive:
                player.health -= 100
                print(f"player = {player.health}")
                self.kill()
                if player.health <= 0:
                    player.update_action(3)
                    player.alive = False

        if pygame.sprite.spritecollide(player3, explosion_group, False):
            player3.alive = False
            print("ggggggggggg")

        if pygame.sprite.spritecollide(Enemy, explosion_group, False):
            if Enemy.alive:
                Enemy.health -= 100
                print(f"player = {Enemy.health}")
                self.kill()
                if Enemy.health <= 0:
                    Enemy.alive = False

        self.rect.x += dx
        self.rect.y += dy

    def dprint(self):
        print("ppppppp")


bullet_group = pygame.sprite.Group()
tir_mazda_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
statics_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

player = Solider(Datas.player_x, Datas.player_y, "Player", 0, 1, 5, 200, 30, 0, True)
gun = Create_Object(player.rect.center, Datas.gun2, 1.25)

player3 = Create_Object((50, 50), Datas.gun2, 2)
Enemy = Solider(Datas.player_x + 300, 283, "Enemyred", 0, 0, 5, 5, 5, 0, False)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    moving_left = False
    moving_right = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        moving_left = True
    if keys[pygame.K_d]:
        moving_right = True
    if keys[pygame.K_SPACE]:
        player.jump = True
    if keys[pygame.K_f]:
        player.shoot()

    player.moving(moving_right, moving_left)

    camera.update(player)

    draw_bg()
    player.update()
    player.draw(camera)
    Enemy.update()
    Enemy.draw(camera)
    gun.update(player.rect.center, player.flip)
    gun.draw(player.flip)

    bullet_group.update()
    bullet_group.draw(Game)
    explosion_group.update()
    explosion_group.draw(Game)

    pygame.display.flip()

pygame.quit()
