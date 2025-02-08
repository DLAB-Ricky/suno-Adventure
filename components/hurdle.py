import pygame
from settings import *

class Hurdle:
    def __init__(self, x, y, speed=DEFAULT_SPEED, size=(90, 90)):
        self.image = pygame.transform.scale(pygame.image.load("assets/images/cac3.png"), size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = x,y
        self.speed = speed

    def move(self):
        """장애물을 왼쪽으로 이동"""
        self.rect.x -= self.speed

    def draw(self, screen):
        """장애물을 화면에 그리기"""
        pygame.draw.rect(screen,(0,255,0), self.rect,2)
        screen.blit(self.image, self.rect)

