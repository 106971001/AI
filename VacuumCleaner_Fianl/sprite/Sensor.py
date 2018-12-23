import pygame
import numpy as np
from enum import Enum

from utils.colorUtils import ColorDictionary as Colors


class SensorType(Enum):
    Laser = 1
    Material = 2


class Sensor(pygame.sprite.Sprite):

    def __init__(self, robot, type=None):
        super().__init__()

        self.type = type
        self.direction = robot.direction
        self.x = robot.x
        self.y = robot.y
        self.value = None

    def update(self, robot):
        self.direction = robot.direction
        self.x = robot.x
        self.y = robot.y

    def get_data(self, env):
        if self.type == SensorType.Laser:
            distance, position = env.get_sensor_laser_data(self)
            self.value = (distance, position)

        if self.type == SensorType.Material:
            env.get_sensor_material_data(self)
