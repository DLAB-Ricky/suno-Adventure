import sys

from pygame.locals import *

from compon:ents.background import Background
from components.dino import Dino
from components.hurdle import Hurdle
from settings import *

pygame.init()

# 사용자 정의 이벤트 ID
TIMER_EVENT = pygame.USEREVENT + 1
WATER_EVENT = pygame.USEREVENT + 2
DINO_EVENT = pygame.USEREVENT + 3
HURDLE_EVENT = pygame.USEREVENT + 4

# 타이머 설정
pygame.time.set_timer(TIMER_EVENT, 5000)
pygame.time.set_timer(HURDLE_EVENT, 2000)
pygame.time.set_timer(WATER_EVENT, 60000)
pygame.time.set_timer(DINO_EVENT, 100)  # DINO_EVENT를 더 자주 실행하도록 설정
speed = DEFAULT_SPEED

max_speed = 25

def auto_increment_score():
    global score, prev_time
    current_time = pygame.time.get_ticks()
    if current_time - prev_time >= 100:
        score += 1
        prev_time = current_time

prev_time = 0
dino_motion_num = 0  # 처음은 0 (dino 노말 상태)

# 초기 설정
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font( None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = Background(WIDTH,HEIGHT)

# Dino 객체 초기화
dino = Dino(20, HEIGHT - GROUND_HEIGHT)

water = {
    "rect": pygame.Rect(800, 290, 60, 60),
    "image": pygame.transform.scale(pygame.image.load("assets/images/water.png"), (70, 70))
}
#1
# 장애물 리스트 초기화
hurdles = []
waterlist = [water]
water_buf_start_time = 0


while True:
    auto_increment_score()

    # 공룡 모드 설정
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == WATER_EVENT:
            water = {
                "rect": pygame.Rect(800, 333, 60, 60),
                "image": pygame.transform.scale(pygame.image.load("assets/images/water.png"), (70, 70))
            }
            waterlist.append(water)
        if event.type == DINO_EVENT:
            dino.animate(speed)
        if event.type == HURDLE_EVENT:
            # 허들 생성
            hurdles.append(Hurdle(WIDTH, HEIGHT - GROUND_HEIGHT + 10))

    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        dino.is_jumping = True

    if score % 100 == 0:
        speed = min(speed +2.5, max_speed)
        pygame.time.set_timer(DINO_EVENT, max(35, 120 - 20 * 2))


    for hurdle in hurdles:
        hurdle.move(speed,1 )
        if hurdle.rect.right < 0:  # 화면을 벗어난 장애물 제거
            hurdles.remove(hurdle)


    """# 물약 이동 및 충돌 체크
    for water in waterlist:
        if dino["rect"].colliderect(water["rect"]):
            dino_motion_num = 1  # giant_dino로 변신
            water_buf_start_time = pygame.time.get_ticks()
            waterlist.remove(water)
        else:
            water["rect"].x -= random.randint(15, 25)

    if dino_motion_num >= 1 and pygame.time.get_ticks() - water_buf_start_time > 10 * SEC and not isjump:
        dino_motion_num = 0

    for water in waterlist:
        screen.blit(water["image"], water["rect"])"""

    # 배경 상태 업데이트
    bg.move(speed)

    # 공룡 상태 업데이트
    dino.jump()
    dino.update_kick()
    dino.check_collision(hurdles)



    # 화면에 그리기
    bg.draw(screen)
    for hurdle in hurdles:
        hurdle.draw(screen)
    dino.draw(screen)


    # 점수 출력
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(min(60, 30 + speed // 2))