import pygame
from settings import *


#클래스
class Hurdle:
    def __init__(self, x, y, speed=DEFAULT_SPEED, size=(90, 90)):
        self.image = pygame.transform.scale(pygame.image.load("assets/images/cac3.png"), size)
        self.blue_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/images/hurdle/hd{i}.png"), size).convert_alpha()
            for i in range(1, 7)
        ]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = x,y
        self.speed = speed
        self.index = 0
        self.frame_counter = 0
        self.frame_delay = 0




    def move(self,speed, option):
        self.frame_delay = max(1, int(DEFAULT_SPEED / speed))  # speed가 높을수록 delay가 줄어듦

        """장애물을 왼쪽으로 이동"""
        self.rect.x -= self.speed
        if option == 0: # 시체
            pass
        elif option == 1: # 파란 : 직진
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.index=(self.index+1) % len(self.blue_frames)
                self.image = self.blue_frames[self.index]
        # elif option == 2: # 빨강 : 점프



    def draw(self, screen):
        """장애물을 화면에 그리기"""
        pygame.draw.rect(screen,(0,255,0), self.rect,2)
        screen.blit(self.image, self.rect)

