import pygame
from time import strftime, gmtime

# Set config and log
from utils.confUtils import CONF as Conf
from utils.confUtils import LOG as Log

# Set RoomEnvironment
from RoomEnvironment import RoomEnvironment
from Visualizer import Visualizer

# Set algorithm
from algorithms import RandomAlgorithm


class Simulator:
    """
    Make a simulator
    1. make a map
    2. set up sprites
    3. draw initial map
    4. loop
        4.1 update robot by algorithms
        4.2 update other sprites
        4.3 update screen
    5. End
    """
    def __init__(self):
        pygame.init()

        # some config
        self.ticks = 0
        self.fps = Conf["simulation"]["fps"]
        self.clock = pygame.time.Clock()
        self.time = strftime("%Y%m%d%H%M%S", gmtime())
        env_conf = Conf["environment"]
        tile_size = env_conf["tile_size"]

        # screen setting
        self.screen = pygame.display.set_mode((env_conf["width"], env_conf["height"]))
        pygame.display.set_caption('Term-Project')
        # self.screen.set_alpha(None)  # What this?
        self.font = pygame.font.Font(None, 20)







        self.environment = RoomEnvironment(env_conf["width"], env_conf["height"], tile_size, env_conf["defaults"]["0"]["obstacles"], env_conf["defaults"]["0"]["robot"])
        self.visualizer = Visualizer(self.environment, self.clock, self.environment.initial_events)
        self.algorithm = RandomAlgorithm()

    def start_simulation(self):
        pass

    def draw(self):
        pass


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start_simulation()
