import pygame
import sys
from time import strftime, gmtime

from utils.confUtils import CONF as Conf
from utils.confUtils import LOG as Log
from utils.colorUtils import ColorDictionary as Colors

from sprite.Tile import Tile
from sprite.Obstacle import Obstacle
from sprite.Robot import Robot

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
        self.algorithm = RandomAlgorithm
        self.show_coverage_path = True  # for display

        # env config
        self.width, self.height, self.tile_size, self.obstacles, self.robot = self.get_env_set()

        # set up sprite groups
        self.group_walls = pygame.sprite.Group()
        self.group_tiles = pygame.sprite.Group()
        self.group_robots = pygame.sprite.Group()

        # screen setting
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Term-Project')
        # self.screen.set_alpha(None)  # What this?
        self.font = pygame.font.Font(None, 20)

        # for statistic
        self.tile_count = 0
        self.covered_tiles = 0
        self.full_covered_tiles = 0

        """
        Initial elements set
        """
        # Set floor and initial walls
        self.initialize_tiles()
        self.initialize_walls()

        # Set customized obstacles and robot
        if self.obstacles is not None:
            self.initialize_customized_obstacles()
        if self.robot is not None:
            self.initialize_customized_robot()

    # For initial environment ------------------------------
    @staticmethod
    def get_env_set():
        """
        Get environment config
        :return: width, height, tile_size
        """
        env_conf = Conf["environment"]
        return env_conf["width"], env_conf["height"], env_conf["tile_size"], env_conf["defaults"]["0"]["obstacles"], \
               env_conf["defaults"]["0"]["robot"]

    def initialize_tiles(self):
        """
        Set all tiles on the map
        :return: None
        """
        for x in range(0, self.width, self.tile_size):
            for y in range(0, self.height, self.tile_size):
                self.group_tiles.add(Tile(x, y, self.tile_size))

    def initialize_walls(self):
        """
                Set initial walls of around
                :return: None
                """
        wall_top = Obstacle(0, 0, self.width, self.tile_size, Colors.BLACK)
        wall_btn = Obstacle(0, self.height - self.tile_size, self.width, self.tile_size, Colors.BLACK)
        wall_left = Obstacle(0, self.tile_size, self.tile_size, self.height - 2 * self.tile_size, Colors.BLACK)
        wall_right = Obstacle(self.width - self.tile_size, self.tile_size, self.tile_size,
                              self.height - 2 * self.tile_size, Colors.BLACK)
        self.group_walls.add(wall_top)
        self.group_walls.add(wall_btn)
        self.group_walls.add(wall_left)
        self.group_walls.add(wall_right)

    def initialize_customized_obstacles(self):
        pass

    def initialize_customized_robot(self):
        self.robot = Robot(self.robot[0], self.robot[1], self.robot[2])
        self.group_robots.add(self.robot)
    # End -------------------------------------------------

    # For drawing on the screen ---------------------------
    def draw_fps(self):
        if Conf["debug"]["draw_fps"]:
            x = 20
            y = 20
            fps = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, Colors.RED)
            self.screen.blit(fps, (x, y))

    def draw_time(self):
        if Conf["debug"]["draw_time"]:
            x = 20
            y = 80
            time = self.font.render("Time: " + str(self.ticks), True, Colors.RED)
            self.screen.blit(time, (x, y))

    def draw_coverage(self):
        if Conf["debug"]["draw_coverage"]:
            x = 20
            y = 40
            coverage_percentage = "20"
            coverage_text = self.font.render("Tile-Coverage: " + str(int(coverage_percentage)) + "%", True, Colors.RED)
            self.screen.blit(coverage_text, (x, y))

            x = 20
            y = 60
            full_coverage_percentage = "80"
            full_coverage_text = self.font.render("Full Tile-Coverage: " + str(int(full_coverage_percentage)) + "%", True, Colors.RED)
            self.screen.blit(full_coverage_text, (x, y))

    def draw_battery(self):
        if Conf["debug"]["draw_battery"]:
            x = 20
            y = 100
            power_text = self.font.render("Power: ", True, Colors.RED)
            self.screen.blit(power_text, (x, y))

            x = x + 60
            y = y - 4
            bar_length = 100
            bar_height = 18
            pct = self.robot.battery_now / self.robot.battery_volume
            fill = pct * bar_length
            outline_rect = pygame.Rect(x, y, bar_length, bar_height)
            fill_rect = pygame.Rect(x, y, fill, bar_height)
            if pct > 0.6:
                col = Colors.GREEN
            elif pct > 0.3:
                col = Colors.YELLOW
            else:
                col = Colors.RED
            pygame.draw.rect(self.screen, col, fill_rect)
            pygame.draw.rect(self.screen, Colors.WHITE, outline_rect, 2)

    def draw_dirt_bag(self):
        if Conf["debug"]["draw_dirt_bag"]:
            x = 20
            y = 120
            dirt_bag_text = self.font.render("Dirt: ", True, Colors.RED)
            self.screen.blit(dirt_bag_text, (x, y))

            x = x + 60
            y = y - 4
            bar_length = 100
            bar_height = 18
            pct = self.robot.dirt_bag_now / self.robot.dirt_bag_volume
            fill = pct * bar_length
            outline_rect = pygame.Rect(x, y, bar_length, bar_height)
            fill_rect = pygame.Rect(x, y, fill, bar_height)
            if pct > 0.6:
                col = Colors.GREEN
            elif pct > 0.3:
                col = Colors.YELLOW
            else:
                col = Colors.RED
            pygame.draw.rect(self.screen, col, fill_rect)
            pygame.draw.rect(self.screen, Colors.WHITE, outline_rect, 2)
    # End --------------------------------------------------

    def get_sensors_data(self, robot_x, robot_y, robot_direction):
        """
        response to sensors of distance and  material of floor
        :return: [] of result
        """

    def pygame_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def start_simulation(self):
        while True:
            self.pygame_events()
            self.update()
            self.draw()

    def update(self):
        self.robot.update(self)
        self.group_walls.update()
        self.group_tiles.update()

    def draw(self):
        self.group_tiles.draw(self.screen)
        self.group_walls.draw(self.screen)
        self.group_robots.draw(self.screen)

        self.draw_fps()
        self.draw_time()
        self.draw_coverage()
        self.draw_battery()
        self.draw_dirt_bag()

        pygame.display.flip()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start_simulation()
