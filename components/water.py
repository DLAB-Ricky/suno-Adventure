import pygame
import random

class Water:
    def __init__(self, x, y, size, image):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.transform.scale(image, (size, size))

    def move(self):
        self.rect.x -= random.randint(15, 25)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
