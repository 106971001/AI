import pygame
import numpy as np
from enum import Enum

from utils.colorUtils import ColorDictionary as Colors


class SensorType(Enum):
    Laser = 1
    Material = 2


class Sensor(pygame.sprite.Sprite):

    def __init__(self, robot, position, sensor_type=None, name=None):
        super().__init__()

        self.type = sensor_type
        self.name = name
        self.direction = robot.direction
        self.x = position[0]
        self.y = position[1]
        self.dx_position_robot = self.x - robot.x
        self.dy_position_robot = self.y - robot.y

        self.value = None

    def update(self, robot):
        self.direction = robot.direction
        self.x = robot.x + self.dx_position_robot
        self.y = robot.y + self.dy_position_robot

    def get_data(self, env):
        if self.type == SensorType.Laser:
            distance, position = env.get_sensor_laser_data(self)
            self.value = (distance, position)

        if self.type == SensorType.Material:
            floor_type = env.get_sensor_material_data(self)
            self.value = floor_type
