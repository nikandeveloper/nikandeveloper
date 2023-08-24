import pygame
from pygame.locals import *
import sys

pygame.init()
main = pygame.display.set_mode((627, 700))
gravity = 15
move = 0
x = 100
y = 100
xchange = 0
img2 = pygame.image.load("ao.png")
img3 = pygame.image.load("alisan.png")
reeect = img3.get_width()
reect = img3.get_height()
reeect2 = img2.get_width()
reect2 = img2.get_height()
pygame.draw.rect()
rect = img3.get_rect()
rect.center = (x, y)
propertis = Rect(x, y, reect, reeect)
propertis2 = Rect(0, 600, reect2, reeect2)
pygame.display.set_caption("fmg")
clock = pygame.time.Clock()
collide = pygame.Rect.colliderect(propertis, propertis2)
while True:
    clock.tick(60)
    x += xchange
    if not collide:
      y += gravity
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              ...
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                xchange = -1
            elif event.key == pygame.K_d:
                xchange = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                xchange = 0
    color = (255, 255, 255)
    main.fill(color)
    pygame.draw.rect(main, "BLUE", propertis)
    pygame.draw.rect(main, "BLUE", propertis2)
    main.blit(img2, (x, y))
    main.blit(img3, (0, 600))
    pygame.display.update()
