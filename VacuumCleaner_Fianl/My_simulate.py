import random
import pygame
import sys

from pygame.locals import *

# Set config and log
from utils.confUtils import CONF as conf
from utils.confUtils import LOG as log

# Set RoomEnvironment
from RoomEnvironment import RoomEnvironment


# Make a Simulator
class Simulator:
    def __init__(self):
        self.event_stream = []
        self.fps = conf["simulation"]["fps"]
        self.clock = pygame.time.Clock()

        # Set Environment, Robot, Visualizer
        env_conf = conf["environment"]
        tile_size = env_conf["tile_size"]

        self.environment = RoomEnvironment(env_conf["width"], env_conf["height"], tile_size, env_conf["defaults"]["0"]["obstacles"], env_conf["defaults"]["0"]["robot"])

    def start_simulation(self):
        pass


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start_simulation()
