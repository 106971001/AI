import pygame
import numpy as np
import math
from enum import Enum

from utils.confUtils import CONF as Conf
from utils.colorUtils import ColorDictionary as Colors

from sprite.Sensor import Sensor, SensorType

from algorithms.RandomAlgorithm import RandomAlgorithmAction


class RobotState(Enum):
    WALK = 1
    ROTATE = 2
    WALK_ROTATE = 3
    STOP = 4
    WALK_BACKWARDS_THEN_ROTATE = 5
    NO_POWER = 6
    FULL_DIRT = 7


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, robot_image_path=None, algorithm=None):
        super().__init__()

        # self picture
        if robot_image_path is None:
            self.image = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
            pygame.draw.circle(self.image, Colors.BLACK, (radius, radius), radius)
            pygame.draw.polygon(self.image, Colors.GREEN, [(0, radius), (2*radius, radius), (radius, 0)])
            pygame.draw.circle(self.image, Colors.BLUE, (radius, radius), 1, 1)
        else:
            self.image = pygame.image.load(robot_image_path).covert()
        self._org_image = self.image

        self.state = RobotState.WALK

        self.rect = self.image.get_rect()
        self._org_rect = self.rect

        # init position
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.angle = 0
        self.angle_delta = 0  # angle to rotate
        self.walk_delta = 0  # distance to walk ?(Maybe don't need)

        # self config
        self.radius = radius
        self.algorithm = algorithm
        self.busy = False  # ?
        self.direction = self.get_direction(self.angle)

        # set walk speed and rotating speed
        self.custom_walk_speed = Conf["robot"]["walk_speed"]
        self.custom_rotate_speed = Conf["robot"]["rotate_speed"]

        # battery function
        self.battery_volume = 1000
        self.battery_now = 500
        self.battery_used_suck = 1
        self.battery_used_walk = 2
        self.battery_used_rot = 3
        self.battery_used_sensors = 4

        # dirt bag function
        self.dirt_bag_volume = 1000
        self.dirt_bag_now = 50

        # path memory function
        self.walked = []

        # sensors
        self.group_sensors = pygame.sprite.Group()
        self.group_sensors.add(Sensor(self, self.rect.midtop, sensor_type=SensorType.Laser, name="head_laser"))
        self.group_sensors.add(Sensor(self, self.rect.midleft, sensor_type=SensorType.Laser, name="left_laser"))
        self.group_sensors.add(Sensor(self, self.rect.midright, sensor_type=SensorType.Laser, name="right_laser"))

    def update(self, env=None):
        """
        1. check state and response
        2. update by algorithm and choose action below
            1. walk
            2. rotate
        """
        if not env:
            pass

        if self.state == RobotState.NO_POWER:
            pass

        if self.state == RobotState.FULL_DIRT:
            pass

        if self.state == RobotState.ROTATE:
            if math.fabs(self.angle_delta) < self.custom_rotate_speed:
                self.angle = (self.angle - self.angle_delta) % 360
                self.angle_delta = 0

                self.direction = self.get_direction(self.angle)
                self.state = RobotState.WALK

            if self.angle_delta > 0:
                self.angle = (self.angle + self.custom_rotate_speed) % 360
                self.angle_delta = self.angle_delta - self.custom_rotate_speed

            if self.angle_delta < 0:
                self.angle = (self.angle - self.custom_rotate_speed) % 360
                self.angle_delta = self.angle_delta + self.custom_rotate_speed

            self.direction = self.get_direction(self.angle)
            self.image = self.rot_center(self._org_image, self.angle % 360 )

        if self.state == RobotState.WALK:
            self.get_sensors_data(env)
            action = self.algorithm.update(self.group_sensors)  # (action_type, action_value)
            if self.algorithm.name == "RandomAlgorithm":
                if action[0] == RandomAlgorithmAction.WALK:
                    self.x += self.custom_walk_speed * self.direction[0]
                    self.rect.x = self.x

                    self.y += self.custom_walk_speed * self.direction[1]
                    self.rect.y = self.y
                if action[0] == RandomAlgorithmAction.ROTATE:
                    self.state = RobotState.ROTATE
                    self.angle_delta = action[1]

        self.group_sensors.update(self)

    def get_direction(self, angle):
        """
        output direction vector in robot unit
        :param angle:
        :return: (dx, dy)
        """
        rad_angle = np.deg2rad((angle+90) % 360)
        return np.round(np.cos(rad_angle), 5),  -np.round(np.sin(rad_angle), 5)

    def get_sensors_data(self, env):
        for sensor in self.group_sensors:
            sensor.get_data(env)

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image


