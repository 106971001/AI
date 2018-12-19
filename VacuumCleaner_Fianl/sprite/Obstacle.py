import pygame
from utils.colorUtils import ColorDictionary as colors


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=colors.BLACK):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_vertex(self, idx:int):
        """
        get position of rect

        3  2
         ┌┐
         └┘
        0  1

        :param idx:
        :return: vertex's position
        """
        idx = idx % 4

        if idx == 0:
            return self.rect.x, self.rect.y + self.height
        elif idx == 1:
            return self.rect.x + self.width, self.rect.y + self.height
        elif idx == 2:
            return self.rect.x + self.width, self.rect.y
        elif idx == 3:
            return self.rect.x + self.rect.y


    def update(self, *args):
        pass