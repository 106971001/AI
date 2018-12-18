


class RooEnvironment:
    def __init__(self, width, height, tile_size, obstacles=None, robot=None):
        self.initial_events = []

        self.obstacles = []
        self.walls = []
        self.tiles = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

    def initialize_tiles(self):
        for x in range(0, self.width, self.tile_size):
            col = []
            for y in range(0, self.height, self.tile_size):
                col.append(Tile(x, y))

            self.tiles.append(col)