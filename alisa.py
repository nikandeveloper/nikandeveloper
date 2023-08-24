import pygame
import sys

pygame.init()
main = pygame.display.set_mode((627, 700))
gravity = 7
move = 0
x = 100
y = 510
xchange = 0
img2 = pygame.image.load("ao.png")
img3 = pygame.image.load("alisan.png")
rect = img3.get_rect()
rect.center = (x, y)
pygame.display.set_caption("fmg")
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    x += xchange
    y -= gravity
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
    main.blit(img2, (q, y))
    main.blit(img3, (0, 600))
    pygame.display.update()
