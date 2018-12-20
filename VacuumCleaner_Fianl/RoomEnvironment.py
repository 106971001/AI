import pygame
from pygame.sprite import Group

from sprite.Tile import Tile
from sprite.Obstacle import Obstacle
from sprite.Robot import Robot

from utils.colorUtils import ColorDictionary as Colors


class RoomEnvironment:

    def __init__(self, width, height, tile_size, obstacles=None, robot=None):
        self.initial_events = []
        self.obstacles = []
        self.group_all_sprites = pygame.sprite.Group()
        self.group_walls = pygame.sprite.Group()
        self.group_tiles = pygame.sprite.Group()
        self.group_robots = pygame.sprite.Group()
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Set floor and initial walls
        self.initialize_tiles()
        self.initialize_walls()

        # Set customized obstacles and robot
        if obstacles is not None:
            self.initialize_customized_obstacles(obstacles)
        if robot is not None:
            self.initialize_customized_robot(robot)

    def initialize_tiles(self):
        """
        Set all tiles on the map
        :return: None
        """
        for x in range(0, self.width, self.tile_size):
            col = []
            for y in range(0, self.height, self.tile_size):
                self.group_tiles.add(Tile(x, y))

    def initialize_walls(self):
        """
        Set initial walls of around
        :return: None
        """
        wall_top = Obstacle(0, 0, self.width, self.tile_size, Colors.BLACK)
        wall_btn = Obstacle(0, self.height - self.tile_size, self.width, self.tile_size, Colors.BLACK)
        wall_left = Obstacle(0, self.tile_size, self.tile_size, self.height - 2*self.tile_size, Colors.BLACK)
        wall_right = Obstacle(self.width - self.tile_size, self.tile_size, self.tile_size, self.height - 2*self.tile_size, Colors.BLACK)

        self.group_walls.add(wall_top)
        self.group_walls.add(wall_btn)
        self.group_walls.add(wall_left)
        self.group_walls.add(wall_right)

    def initialize_customized_obstacles(self, obstacles):
        pass

    def initialize_customized_robot(self, robot):
        self.robot = Robot(robot[0], robot[1], robot[2])
        self.group_robots.add(self.robot)




