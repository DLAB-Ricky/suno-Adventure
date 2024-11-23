import pygame, sys
from pygame.locals import *
import random

pygame.init()

# 사용자 정의 이벤트 ID
TIMER_EVENT = pygame.USEREVENT + 1
WATER_EVENT = pygame.USEREVENT + 2
DINO_EVENT = pygame.USEREVENT + 3
"""
허들 타이머 설정: 5000ms마다 TIMER_EVENT 이벤트 발생
물컵 타이머 설정: 30000ms마다 WATER_EVENT 이벤트 발생
"""
pygame.time.set_timer(TIMER_EVENT, 5000)
pygame.time.set_timer(WATER_EVENT, 30000)
pygame.time.set_timer(DINO_EVENT, 100)

def auto_increment_score():
    global score, prev_time
    current_time = pygame.time.get_ticks()
    if current_time - prev_time >= 100:
        score += 1
        prev_time = current_time

prev_time = 0
giant = False

# 화면 크기
WIDTH = 1000
HEIGHT = 800
# 시간
SEC = 1000
# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 위치
GROUND_HEIGHT = 407

# 공룡 크기
NORMAL_DINO = 60
GIANT_DINO = 120

clock = pygame.time.Clock()


score = 0
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


bgimage = pygame.image.load("real-bg.png")
bgimage = pygame.transform.scale(bgimage, (WIDTH, HEIGHT))

dino_right = pygame.transform.scale(pygame.image.load("dino.png"), (70, 70))
dino_left = pygame.transform.scale(pygame.image.load("dino2.png"), (70, 70))

giant_dino_right = pygame.transform.scale(pygame.image.load("dino.png"), (140, 140))
giant_dino_left = pygame.transform.scale(pygame.image.load("dino2.png"), (140, 140))

dino = {
    "rect": pygame.draw.rect(screen, WHITE, (20, HEIGHT - GROUND_HEIGHT - NORMAL_DINO, NORMAL_DINO, NORMAL_DINO)),
    "giant_rect": pygame.draw.rect(screen, WHITE, (20, HEIGHT - GROUND_HEIGHT - GIANT_DINO, GIANT_DINO, GIANT_DINO)),
    "image": dino_left,
    "giant_image": giant_dino_left
}

water = {
    "rect": pygame.draw.rect(screen, WHITE, (800, 333, 60, 60)),
    "image": pygame.transform.scale(pygame.image.load("물컵2.0.png"), (70, 70))
}


hurdlelist = []
waterlist = [water]

isjump = False
jumpstep = 10
backX = 0
backX2 = WIDTH

water_buf_start_time = 0

while True:
    auto_increment_score()
    mode = ["rect", "giant_rect"][giant]
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == TIMER_EVENT:
            hurdle = {
                "rect": pygame.draw.rect(screen, WHITE, (800, 333, 60, 60)),
                "image": pygame.transform.scale(pygame.image.load("선인장 인데요.png"), (60, 60))
            }
            hurdlelist.append(hurdle)
        if event.type == WATER_EVENT:
            water = {
                "rect": pygame.draw.rect(screen, WHITE, (800, 333, 60, 60)),
                "image": pygame.transform.scale(pygame.image.load("물컵2.0.png"), (70, 70))
            }
            waterlist.append(water)
        if event.type == DINO_EVENT:
            if giant:
                if dino["giant_image"] == giant_dino_left:
                    dino["giant_image"] = giant_dino_right
                else:
                    dino["giant_image"] = giant_dino_left
            else:
                if dino["image"] == dino_left:
                    dino["image"] = dino_right
                else:
                    dino["image"] = dino_left


    keyinput = pygame.key.get_pressed()
    if keyinput[K_SPACE]:
        isjump = True

    backX -= 10
    backX2 -= 10

    # 점프 기능
    if isjump:
        if jumpstep >= - 10:
            dino[["rect", "giant_rect"][giant]].top -= jumpstep * abs(jumpstep)
            jumpstep -= 1
        else:
            isjump = False
            jumpstep = 10

    if backX < WIDTH * -1:
        backX = WIDTH - 100
    if backX2 < WIDTH * -1:
        backX2 = WIDTH - 100

    for hurdle in hurdlelist:
        # 허들
        if dino[mode].colliderect(hurdle["rect"]):
            if not giant:
                pygame.quit()
                sys.exit()
            hurdlelist.remove(hurdle)
        else:
            hurdle["rect"].x -= 10


    # 물약
    for water in waterlist:
        if dino['rect'].colliderect(water["rect"]):
            giant = True
            water_buf_start_time = prev_time
            waterlist.remove(water)
            prev_time = pygame.time.get_ticks()
        else:
            water["rect"].x -= random.randint(15, 25)
    if giant and water_buf_start_time + 10 * SEC < pygame.time.get_ticks() and isjump == False:
        giant = False

    screen.blit(bgimage, (backX, 0))
    screen.blit(bgimage, (backX2, 0))
    for water in waterlist:
        screen.blit(water["image"], water["rect"])
    for hurdle in hurdlelist:
        screen.blit(hurdle["image"], hurdle["rect"])
    score_text = font.render(f"Score:{score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(dino[["image", "giant_image"][giant]], dino[["rect", "giant_rect"][giant]])

    pygame.display.update()

# 게임 종료
pygame.quit()
sys.exit()