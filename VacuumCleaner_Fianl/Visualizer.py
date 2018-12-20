import pygame
from time import strftime, gmtime


class Visualizer:
    def __init__(self, env, clock, initial_events):
        pygame.init()

        self.ticks = 0
        self.clock = clock

        # Screen Setting
        self.screen = pygame.display.set_mode((env.width, env.height))
        pygame.display.set_caption('Term-Project')
        # self.screen.set_alpha(None)  # What this?
        self.font = pygame.font.Font(None, 20)

        # sprites group
        self.group_all_sprites = env.group_all_sprites
        self.group_tiles = env.group_tiles
        self.group_walls = env.group_walls
        self.group_robots = env.group_robots

        # for statistic
        self.tile_count = 0
        self.covered_tiles = 0
        self.full_covered_tiles = 0
        self.stats = []

        # for display
        self.show_coverage_path = True

        self.time = strftime("%Y%m%d%H%M%S", gmtime())