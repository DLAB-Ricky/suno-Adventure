import pygame

class Background:
    def __init__(self, width, height):
        self.image = pygame.image.load("assets/images/hell.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x1 = 0
        self.x2 = width
        self.width = width

    def move(self, speed):
        self.x1 -= speed
        self.x2 -= speed
        if self.x1 <= -self.width:
            self.x1 = self.width
        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))

