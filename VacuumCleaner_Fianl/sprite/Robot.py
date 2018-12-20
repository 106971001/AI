import pygame
import numpy as np
from enum import Enum

from utils.confUtils import CONF as Conf
from utils.colorUtils import ColorDictionary as Colors


class RobotState(Enum):
    WALK = 1
    ROTATE = 2
    WALK_ROTATE = 3
    STOP = 4
    WALK_BACKWARDS_THEN_ROTATE = 5
    NO_POWER = 6
    FULL_DIRT = 7


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, robot_image_path=None):
        super().__init__()

        # self picture
        if robot_image_path is None:
            self.image = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
            pygame.draw.circle(self.image, Colors.BLACK, (radius, radius), radius)
            pygame.draw.polygon(self.image, Colors.GREEN, [(0, radius), (2*radius, radius), (radius, 0)])
        else:
            self.image = pygame.image.load(robot_image_path).covert()
        self._org_image = self.image

        self.state = RobotState.STOP

        self.rect = self.image.get_rect()
        self._org_rect = self.rect

        # init position
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.angle = 0
        self.angle_delta = 0  # angle to rotate
        self.walk_delta = 0  # distance to walk ?(Maybe don't need)

        self.radius = radius
        self.busy = False  # ?
        self.direction = self._get_direction(self.angle)

        # set walk speed and rotating speed
        self.walk_speed = Conf["robot"]["walk_speed"]
        self.rotate_speed = Conf["robot"]["rotate_speed"]
        self.custom_walk_speed = self.walk_speed
        self.custom_rotate_speed = self.rotate_speed

        # battery function
        self.battery_volume = 1000
        self.battery_used_suck = 1
        self.battery_used_walk = 2
        self.battery_used_rot = 3
        self.battery_used_sensors = 4

        # path memory function
        self.walked = []

    def update(self):
        pass



    def _get_direction(self, angle):
        """
        output direction vector in robot unit
        :param angle:
        :return: (dx, dy)
        """
        rad_angle = np.deg2rad((angle+90) % 360)
        return np.round(np.cos(rad_angle), 5),  np.round(np.sin(rad_angle), 5)


