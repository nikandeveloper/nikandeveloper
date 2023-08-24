import pygame
from pygame.locals import *

pygame.init()

size = Width, hieght = 800, 450
Game = pygame.display.set_mode(size)
pygame.display.set_caption("Home-coming")

moving_left = False
moving_right = False
moving_up = False
moving_down = False
clock = pygame.time.Clock()
FPS = 60
BG = (144, 201, 120)

def draw_bg():
    Game.fill(BG)

class Solider(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animations = []
        self.frame_index = 0
        action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(10):
         img = pygame.image.load(f"Images/{self.char_type}/pixil-frame-0 ({i}).png")
         self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
         self.animations.append(img)
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        Animation_cooldown = 100
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > Animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

    def moving(self, moving_right, moving_left):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = 1
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = -1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        Game.blit(pygame.transform.flip(self.image, self.flip, False) ,self.rect)


x = 200
y = 200
scale = 0.25

player = Solider(x, y, "Player",scale, 5)

edame = True

while edame:
    draw_bg()
    clock.tick(FPS)
    player.update_animation()
    player.draw()
    player.moving(moving_right, moving_left)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            edame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()