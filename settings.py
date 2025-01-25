import pygame
# 화면 크기
WIDTH = 1000
HEIGHT = 360

# 시간, 색상
SEC = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 위치 및 크기
GROUND_HEIGHT = 11
NORMAL_DINO = 60
GIANT_DINO = 120

# 시간 이벤트
TIMER_EVENT = pygame.USEREVENT + 1
WATER_EVENT = pygame.USEREVENT + 2
DINO_EVENT = pygame.USEREVENT + 3