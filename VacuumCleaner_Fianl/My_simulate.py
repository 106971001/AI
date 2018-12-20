import random
import pygame
import sys

from pygame.locals import *

# Set config and log
from utils.confUtils import CONF as Conf
from utils.confUtils import LOG as log

# Set RoomEnvironment
from RoomEnvironment import RoomEnvironment
from Visualizer import Visualizer


class Simulator:
    """
    Make a simulator
    1. make map and collect initial events
        1.1 setup map with sprite(robot, tiles, walls....)
    2. make visualizer and draw with initial events
    3. update map and collect modify events
    4. update screen with modify events by visualizer
    5. End
    """
    def __init__(self):
        self.event_stream = []
        self.fps = Conf["simulation"]["fps"]
        self.clock = pygame.time.Clock()

        # Set Environment, Robot, Visualizer
        env_conf = Conf["environment"]
        tile_size = env_conf["tile_size"]

        self.environment = RoomEnvironment(env_conf["width"], env_conf["height"], tile_size, env_conf["defaults"]["0"]["obstacles"], env_conf["defaults"]["0"]["robot"])
        self.visualizer = Visualizer(self.environment, self.clock, self.environment.initial_events)

    def start_simulation(self):
        pass


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start_simulation()
