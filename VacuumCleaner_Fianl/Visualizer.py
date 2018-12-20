import pygame
from time import strftime, gmtime

from events.EventType import EventType

from sprite.Tile import TileState

from utils.confUtils import CONF as Conf
from utils.confUtils import LOG as Log
from utils.colorUtils import ColorDictionary as Colors


class Visualizer:
    def __init__(self, env, clock, initial_events):
        pygame.init()

        # some config
        self.ticks = 0
        self.clock = clock
        self.time = strftime("%Y%m%d%H%M%S", gmtime())

        # screen setting
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

        # initial screen elements
        self.handler_simulator_events(initial_events)

    def handler_simulator_events(self, events):
        for event in events:
            if event.type == EventType.OBSTACLE_ADDED:
                Log.info("Add Obstacle " + str(event.new_obstacle))
                self.group_obstacles.add(event.new_obstacle)
            if event.type == EventType.ROBOT_PLACED:
                Log.info("Robot placed " + str(event.placed_robot))
                self.group_robots.add(event.placed_robot)
            if event.type == EventType.TILE_COVERED:
                if event.is_first_cover():
                    self.covered_tiles = self.covered_tiles + 1
                    self.group_tiles.add(event.tile)
                if event.tile.state == TileState.FULL_COVERED:
                    self.full_covered_tiles = self.full_covered_tiles + 1
                    self.group_tiles.add(event.tile)
            if event.type == EventType.TILE_COVERED_BY_OBSTACLE:
                self.group_tiles.add(event.tile)

    def draw(self):

        dirt = Conf["simulation"].get("dirt", 35)
        base_color = [255 - dirt, 255 - dirt, 255 - dirt]
        self.screen.fill(base_color)

        self.group_tiles.update()
        self.group_walls.update()
        self.group_robots.update()

        self.group_tiles.draw(self.screen)
        self.group_walls.draw(self.screen)
        self.group_robots.draw(self.screen)

        self.draw_fps()
        self.draw_time()

        pygame.display.flip()

    def draw_fps(self):
        if Conf["debug"]["draw_fps"]:
            fps = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, Colors.RED)
            self.screen.blit(fps, (20, 20))

    def draw_time(self):
        if Conf["debug"]["draw_time"] :
            time = self.font.render("Time: " + str(self.ticks), True, Colors.RED)
            self.screen.blit(time, (20, 80))

