import pygame as pg
import sys
import heapq

from os import path
from config import *
from sprites import *
from tilemap import *

vec = pg.math.Vector2

def draw_robot_power(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_robot_dirt(surf, x, y, volum):
    if volum > 100:
        pct = 100
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = volum
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

    pg.draw.rect(surf, WHITE, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)


def draw_text(surf, text, size, color, x, y, align="nw"):
    font_name = pg.font.match_font('hack')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


def vec2int(v):
    return int(v.x), int(v.y)


def heuristic(a, b):
    # return abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2
    return (abs(a.x - b.x) + abs(a.y - b.y)) * 10


def a_star_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost + heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path, cost


def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path, cost


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0


class Game:
    def __init__(self):
        pg.init()

        # load data
        self.map = ''
        self.map_img = ''
        self.map_rect = ''
        self.robot_img = ''
        self.item_images = ''

        # initial
        self.all_sprites = ''
        self.robot = ''
        self.walls = ''
        self.items = ''
        self.camera = ''
        self.draw_debug = ''

        self.output_string = ''
        self.frame_count = 0
        self.hit_dirt = 0
        self.obstacle = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        self.weights = {}
        self.home = vec(49,47)

        # running
        self.playing = False
        self.dt = ''
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.font = pg.font.Font(None, 30)
        self.start = False

    def in_bounds(self, node):
        return 0 <= node.x < WIDTH and 0 <= node.y < HEIGHT

    def passable(self, node):
        return node not in self.obstacle

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

    def find_path(self, start, goal):

        total_path, c = a_star_search(g, goal, start)

        best_path = self.go_to_target(start, goal, total_path)
        return best_path

    def go_to_target(self, start, goal, path):
        # draw path from start to goal
        best_path = []
        current = start  # + path[vec2int(start)]
        l = 0
        while current != goal:
            v = path[(current.x, current.y)]
            if v.length_squared() == 1:
                l += 10
            else:
                l += 14
            # find next in path
            current = current + path[vec2int(current)]
            best_path.append(current)
        return best_path

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        music_folder = path.join(game_folder, 'music')
        self.map = TiledMap(path.join(map_folder, 'copyhome.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.robot_img = pg.image.load(path.join(img_folder, ROBOT_IMG)).convert_alpha()
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width /2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.robot = Robot(self, obj_center.x, obj_center.y)  # init robot
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.obstacle.append(vec(int(tile_object.x/TILE_SIZE), int(tile_object.y/TILE_SIZE)))
            if tile_object.name in ['dirt','Ddirt','battery']:
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_s:
                    if self.robot.mode == RobotMode.Manual:
                        self.robot.mode = RobotMode.Auto
                    elif self.robot.mode == RobotMode.Auto:
                        self.robot.mode = RobotMode.Manual
                if event.key == pg.K_n:
                    self.new()
                    self.run()
                if event.key == pg.K_b:
                    if self.robot.mode == RobotMode.Manual:
                        if self.robot.algorithm == 'RANDOM':
                            self.robot.algorithm = 'SWALK'
                        else:
                            self.robot.algorithm = 'RANDOM'
                if event.key == pg.K_c:
                    if self.robot.mode == RobotMode.Manual:
                        self.robot.dirt = 0

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.robot)

        # battery update
        # 10 second & dirt 10 minus 1% if self.clock
        TOTAL_SECONDS = self.frame_count // FPS
        minutes = TOTAL_SECONDS // 60
        seconds = TOTAL_SECONDS % 60
        self.frame_count +=1
        if self.robot.dirt >= 0:
            # minus_time = int(pg.time.get_ticks()/1000)/20
            if int(seconds/10) in NUMBERS and int(seconds/10) > 0:
                if self.robot.power != 0:
                    self.robot.power -= BATTERY_CAHRGE/1000

        # player hits items
        hits = pg.sprite.spritecollide(self.robot, self.items, False)
        for hit in hits:
            if hit.type == 'dirt' and self.robot.dirt < 100 and self.robot.power > 15:
                hit.kill()
                self.hit_dirt += 1
                self.robot.add_dirt(DIRT_COLLECT)
                if self.robot.dirt != 0:   
                    self.robot.minus_battery(BATTERY_CAHRGE,5) 
            if hit.type == 'Ddirt' and self.robot.dirt < 100 and self.robot.power > 15:
                hit.kill()
                self.hit_dirt += 1
                self.robot.add_dirt(DDIRT_COLLECT)
                if self.robot.dirt != 0:
                    self.robot.minus_battery(BATTERY_CAHRGE,2) 
                keys = pg.key.get_pressed()
                if keys[pg.K_UP] or keys[pg.K_w]:
                    self.robot.vel = vec(100, 0).rotate(-self.robot.rot)
            if hit.type == 'battery' and self.robot.dirt == 100:
                self.robot.dirt = 0

            elif hit.type == 'battery' and self.robot.power < 15:
                self.robot.dirt = 0
                self.robot.power = 100

            elif hit.type == 'battery' and self.robot.power < 15 and self.robot.dirt == 100:
                self.robot.dirt = 0
                self.robot.power = 100

    def draw(self):
        pg.display.set_caption(TITLE)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        draw_robot_power(self.screen, 10, 10, self.robot.power / ROBOT_POWER)
        draw_text(self.screen, str(int(self.robot.power))+ "%", 30, BLACK, 120, 10)
        draw_robot_dirt(self.screen, 10, 40, self.robot.dirt)
        draw_text(self.screen, "clean_rate:"+str(int((self.hit_dirt/TOTAL_DIRTS)*100))+ "%", 30, BLACK, 10, 70)
        draw_text(self.screen, str(int(self.robot.dirt)), 30, BLACK, 120, 40)
        # draw_text(self.screen, self.output_string, 30, RED, WIDTH-120, 60
        draw_text(self.screen, "Time: " + str(pg.time.get_ticks()/1000), 30, RED, WIDTH-120, 10)
        draw_text(self.screen, str(self.robot.pos/TILE_SIZE), 30, WHITE, WIDTH - 160, 40)

        draw_text(self.screen, self.robot.algorithm, 30, BLACK, 10, 100)

        pg.display.flip()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()


# create the game object
g = Game()
while True:
    g.new()
    g.run()
