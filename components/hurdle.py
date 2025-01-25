import pygame

class Hurdle:
    def __init__(self, x, y, speed=20,size=(90, 90)):
        self.image = pygame.transform.scale(pygame.image.load("assets/images/cac3.png"), size)
        self.rect = pygame.Rect(x, y - size[1], size[0], size[1])
        self.speed = speed

    def move(self):
        """장애물을 왼쪽으로 이동"""
        self.rect.x -= self.speed

    def draw(self, screen):
        """장애물을 화면에 그리기"""
        screen.blit(self.image, self.rect)

