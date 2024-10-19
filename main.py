import pygame, sys
from pygame.locals import *
import random

pygame.init()

def auto_increment_score():
    global score, prev_time
    current_time = pygame.time.get_ticks()
    if current_time - prev_time >= 100:
        score += 1
        prev_time = current_time


WIDTH = 1000
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()


score = 0
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

dino = pygame.draw.rect(screen, WHITE, (20, 570, 70, 70))

hurdle = pygame.draw.rect(screen, WHITE, (1000, 570, 35, 70))

prev_time = pygame.time.get_ticks()
isjump = False
jumpstep = 10

while True:
    pygame.time.delay(15)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    hurdle.x -= 10

    keyinput = pygame.key.get_pressed()
    if keyinput[K_UP] and dino.top >= 0:
        dino.top -= 5
    elif keyinput[K_DOWN] and dino.bottom <= HEIGHT:
        dino.bottom += 5

    if keyinput[K_SPACE]:
        isjump = True

    if isjump:
        if jumpstep >= -10:
            dino.top -= jumpstep * abs(jumpstep)
            jumpstep -= 1
        else:
            isjump = False
            jumpstep = 10

    clock.tick(60)

    auto_increment_score()
    pygame.draw.rect(screen, WHITE, dino)
    pygame.draw.rect(screen, WHITE, hurdle)
    score_text = font.render(f"Score:{score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()