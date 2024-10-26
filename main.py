import pygame, sys
from pygame.locals import *
import random

pygame.init()

# def auto_increment_score():
#     global score, prev_time
#     current_time = pygame.time.get_ticks()
#     if current_time - prev_time >= 100:
#         score += 1
#         prev_time = current_time


WIDTH = 1000
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()


score = 0
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bgimage = pygame.image.load("real-bg.png")
bgimage = pygame.transform.scale(bgimage, (WIDTH, HEIGHT))
dino = {
    "rect": pygame.draw.rect(screen, WHITE, (20, 333, 60, 60)),
    "image": pygame.transform.scale(pygame.image.load("dino.png"), (70,70))
}

hurdle = pygame.draw.rect(screen, WHITE, (1000, 570, 35, 70))


isjump = False
jumpstep = 10
backX = 0
backX2 = WIDTH

while True:
    pygame.time.delay(3)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    hurdle.x -= 10

    keyinput = pygame.key.get_pressed()
    if keyinput[K_UP] and dino["rect"].top >= 0:
        dino["rect"].top -= 5
    elif keyinput[K_DOWN] and dino["rect"].bottom <= HEIGHT:
        dino["rect"].bottom += 5

    if keyinput[K_SPACE]:
        isjump = True

    backX -= 8
    backX2 -= 8

    # 점프 기능
    if isjump:
        if jumpstep >= -10:
            dino["rect"].top -= jumpstep * abs(jumpstep)
            jumpstep -= 1
        else:
            isjump = False
            jumpstep = 10

    if backX < WIDTH * -1:
        backX = WIDTH
    if backX2 < WIDTH * -1:
        backX2 = WIDTH


    # auto_increment_score()
    screen.blit(bgimage, (backX, 0))
    screen.blit(bgimage, (backX2, 0))
    pygame.draw.rect(screen, WHITE, dino['rect'])
    pygame.draw.rect(screen, WHITE, hurdle)
    score_text = font.render(f"Score:{score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(dino["image"], dino["rect"])
    pygame.display.update()