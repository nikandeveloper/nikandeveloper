import pygame
import sys
pygame.init()
x_display = 550
y_display = 610
main = pygame.display.set_mode((x_display, y_display))
whate_c = (255,255,255)
main_img0 = pygame.transform.scale2x(pygame.image.load("S0.png"))
main_img1 = pygame.transform.scale2x(pygame.image.load("S1.png"))
main_img2 = pygame.transform.scale2x(pygame.image.load("S2.png"))
main_imgF = pygame.image.load("alisan 1.png")
x_change = 0
x = 100
xF = 0
clock = pygame.time.Clock()
while True:
    x += x_change
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_change = -3
            elif event.key == pygame.K_d:
                x_change = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x_change = 0
    pygame.display.update()
    main.fill(whate_c)
    xF -= 1
    main.blit(main_img0, (x, 330))
    main.blit(main_imgF, (xF, 510))
    main.blit(main_imgF, (xF + 550, 510))
    if xF <= -550 :
        xF = 0
clock.tick(60)