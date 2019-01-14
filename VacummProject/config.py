import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "VacuumCleaner Demo"
BGCOLOR = BROWN

TILE_SIZE = 32
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE


# Robot settings
ROBOT_POWER = 100
ROBOT_DIRT = 0
ROBOT_SPEED = 150
ROBOT_ROT_SPEED = 100
ROBOT_IMG = 'hoover-robot.png'
ROBOT_HIT_RECT = pg.Rect(0, 0, 50, 50) # fix rec size to avoid hit wall problem
DIRT_COLLECT = 1
DDIRT_COLLECT = 3

# RANDOM,
ROBOT_ALGORITHM = "SWALK"

# Layers
WALL_LAYER = 1
ROBOT_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'dirt': 'dirt.png','Ddirt':'ddirt.png'}
ITEM_HIT_RECT = pg.Rect(0, 0, 35, 35)