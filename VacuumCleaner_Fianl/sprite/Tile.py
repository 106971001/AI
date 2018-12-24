import pygame

from enum import Enum

from utils.colorUtils import ColorDictionary as colors
from utils.confUtils import CONF as conf


class TileState(Enum):
    UNCOVERED = 0
    COVERED = 1
    FULL_COVERED = 2
    COVERED_BY_OBSTACLE = 3


class TileType(Enum):
    Normal = 1
    Enforce = 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, tile_size: int):
        super().__init__()
        self.x = x
        self.y = y
        self.width = tile_size
        self.height = tile_size
        self.color = colors.LIGHT_GREY
        self.state = TileState.UNCOVERED
        self.floor_type = TileType.Normal

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((220, 220, 220))

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

    def set_floor_type(self, floor_type: TileType):
        self.floor_type = floor_type

    def update(self, *args):
        pass
