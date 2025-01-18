import pygame, sys
from pygame.locals import *
import random

pygame.init()

# 사용자 정의 이벤트 ID
TIMER_EVENT = pygame.USEREVENT + 1
WATER_EVENT = pygame.USEREVENT + 2
DINO_EVENT = pygame.USEREVENT + 3

# 타이머 설정
pygame.time.set_timer(TIMER_EVENT, 5000)
pygame.time.set_timer(WATER_EVENT, 60000)
pygame.time.set_timer(DINO_EVENT, 50)  # DINO_EVENT를 더 자주 실행하도록 설정
speed = 20
ping = 100

def auto_increment_score():
    global score, prev_time
    current_time = pygame.time.get_ticks()
    if current_time - prev_time >= 100:
        score += 1
        prev_time = current_time

prev_time = 0
dino_motion_num = 0  # 처음은 0 (dino 노말 상태)

# 화면 크기
WIDTH = 1000
HEIGHT = 800

# 시간, 색상
SEC = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 위치 및 크기
GROUND_HEIGHT = 410
NORMAL_DINO = 60
GIANT_DINO = 120

# 초기 설정
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 이미지 로드
bgimage = pygame.image.load("assets/images/background.png")
bgimage = pygame.transform.scale(bgimage, (WIDTH, HEIGHT))

# 공룡 이미지 리스트 (정상 크기, 거대 크기)
dino_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/images/dino{i}.png"), (80, 80)) for i in range(1, 7)
]
giant_dino_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/images/dino{i}.png"), (160, 160)) for i in range(1, 7)
]
giant_dino_kick_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/images/kick{i}.png"), (160, 160)) for i in range(1, 7)
]

# 공룡 객체
dino = {
    "rect": pygame.Rect(20, HEIGHT - GROUND_HEIGHT - NORMAL_DINO, NORMAL_DINO, NORMAL_DINO),
    "giant_rect": pygame.Rect(20, HEIGHT - GROUND_HEIGHT - GIANT_DINO, GIANT_DINO, GIANT_DINO),
    "giant_kick_rect": pygame.Rect(20, HEIGHT - GROUND_HEIGHT - GIANT_DINO, GIANT_DINO, GIANT_DINO),
    "current_frame": 0
}

water = {
    "rect": pygame.Rect(800, 333, 60, 60),
    "image": pygame.transform.scale(pygame.image.load("assets/images/water.png"), (70, 70))
}

hurdlelist = []
waterlist = [water]

isjump = False
jumpstep = 7
backX = 0
backX2 = WIDTH
water_buf_start_time = 0

kick_frame = 0  # 킥 모션 프레임

while True:
    auto_increment_score()

    # 공룡 모드 설정
    mode = ["rect", "giant_rect", "giant_kick_rect"][dino_motion_num]
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == TIMER_EVENT:
            hurdle = {
                "rect": pygame.Rect(800, 328, 80, 80),
                "image": pygame.transform.scale(pygame.image.load("assets/images/cac2.png"), (80, 80))
            }
            hurdlelist.append(hurdle)
        if event.type == WATER_EVENT:
            water = {
                "rect": pygame.Rect(800, 333, 60, 60),
                "image": pygame.transform.scale(pygame.image.load("assets/images/water.png"), (70, 70))
            }
            waterlist.append(water)
        if event.type == DINO_EVENT:
            # 공룡의 상태에 맞게 current_frame 갱신
            if dino_motion_num == 0:
                dino["current_frame"] = (dino["current_frame"] + 1) % len(dino_frames)
            elif dino_motion_num == 1:
                dino["current_frame"] = (dino["current_frame"] + 1) % len(giant_dino_frames)
            elif dino_motion_num == 2:
                if kick_frame < len(giant_dino_kick_frames) - 1:
                    kick_frame += 1  # kick 모션을 더 빠르게 진행
                else:
                    dino_motion_num = 0  # 킥이 끝나면 다시 정상 상태로

    keyinput = pygame.key.get_pressed()
    if keyinput[K_SPACE]:
        isjump = True

    backX -= speed
    backX2 -= speed
    if score % 100 == 0:
        speed += 2.5
        ping += 25
        pygame.time.set_timer(DINO_EVENT, 35)

    # 점프 기능
    if isjump:
        if jumpstep >= -7:
            dino[mode].top -= jumpstep * abs(jumpstep)
            jumpstep -= 1
        else:
            isjump = False
            jumpstep = 7

    # 배경 이동
    if backX < -WIDTH:
        backX += 2 * WIDTH
    if backX2 < -WIDTH:
        backX2 += 2 * WIDTH

    # 허들 이동 및 충돌 체크
    for hurdle in hurdlelist:
        if dino[mode].colliderect(hurdle["rect"]):
            if dino_motion_num == 0:
                pygame.quit()
                sys.exit()
            elif dino_motion_num == 1:
                dino_motion_num = 2

            hurdlelist.remove(hurdle)
        else:
            hurdle["rect"].x -= speed

    # 물약 이동 및 충돌 체크
    for water in waterlist:
        if dino["rect"].colliderect(water["rect"]):
            dino_motion_num = 1  # giant_dino로 변신
            water_buf_start_time = pygame.time.get_ticks()
            waterlist.remove(water)
        else:
            water["rect"].x -= random.randint(15, 25)

    if dino_motion_num >= 1 and pygame.time.get_ticks() - water_buf_start_time > 10 * SEC and not isjump:
        dino_motion_num = 0

    # 배경 및 오브젝트 그리기
    screen.blit(bgimage, (backX, 0))
    screen.blit(bgimage, (backX2, 0))
    for water in waterlist:
        screen.blit(water["image"], water["rect"])
    for hurdle in hurdlelist:
        screen.blit(hurdle["image"], hurdle["rect"])

    # 현재 공룡 이미지 렌더링
    if dino_motion_num == 0:
        current_dino_image = dino_frames[dino["current_frame"]]
    elif dino_motion_num == 1:
        current_dino_image = giant_dino_frames[dino["current_frame"]]
    elif dino_motion_num == 2:
        current_dino_image = giant_dino_kick_frames[kick_frame]

    screen.blit(current_dino_image, dino[mode])

    # 점수 출력
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)