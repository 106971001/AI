from sprite.Tile import Tile
from sprite.Obstacle import Obstacle
from utils.colorUtils import ColorDictionary as colors


class RoomEnvironment:
    def __init__(self, width, height, tile_size, obstacles=None, robot=None):
        self.initial_events = []

        self.obstacles = []
        self.walls = []
        self.tiles = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Set floor and initial walls
        self.initialize_tiles()
        self.initial_events.extend(self.initialize_walls())

    def initialize_tiles(self):
        for x in range(0, self.width, self.tile_size):
            col = []
            for y in range(0, self.height, self.tile_size):
                col.append(Tile(x, y))

            self.tiles.append(col)

    def initialize_walls(self):
        wall_top = Obstacle(0, 0, self.width, self.tile_size, colors.BLACK)
        wall_btn = Obstacle(0, self.height - self.tile_size, self.width, self.tile_size, colors.BLACK)
        wall_left = Obstacle(0, self.tile_size, self.tile_size, self.height - 2*self.tile_size, colors.BLACK)
        wall_right = Obstacle(self.width - self.tile_size, self.tile_size, self.tile_size, self.height - 2*self.tile_size, colors.BLACK)

        self.walls.append(wall_top)
        self.walls.append(wall_btn)
        self.walls.append(wall_left)
        self.walls.append(wall_right)



