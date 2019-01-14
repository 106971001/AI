import math
import random
from enum import Enum

from config import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2


# in order not appear gap when collide, so check two direction
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect) # collide_hit_rec define in tilemap.py
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2  # avoid rotate problem
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x                            # avoid rotate problem

            if sprite.state == RobotState.SWALK_go_1_2:
                sprite.state = RobotState.SWALK_and_HITWALL
            else:
                sprite.state = RobotState.HITWALL

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2 #hit top of the block 
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y                # use centery avoid rotate problem

            if sprite.state == RobotState.SWALK_go_1_2:
                sprite.state = RobotState.SWALK_and_HITWALL
            elif  sprite.state == RobotState.SWALK_rot_1:
                sprite.state == RobotState.SWALK_rot_1_and_HITWALL
            elif sprite.state == RobotState.SWALK_rot_2:
                sprite.state == RobotState.SWALK_rot_2_and_HITWALL
            else:
                sprite.state = RobotState.HITWALL


class RobotMode(Enum):
    Manual = 1
    Auto = 2


class RobotState(Enum):
    STOP = 1
    RUNNING = 2
    HITWALL = 3

    SWALK_rot_1 = 4
    SWALK_rot_2 = 5
    SWALK_go_1_2 = 6
    SWALK_and_HITWALL = 7
    SWALK_rot_1_and_HITWALL = 8
    SWALK_rot_2_and_HITWALL = 9


class Robot(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ROBOT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.robot_img
        self.rect = self.image.get_rect()
        self.hit_rect = ROBOT_HIT_RECT                # fix rec size to avoid hit wall problem
        self.hit_rect.center = self.rect.center       # fix rec size to avoid hit wall problem

        self.vel = vec(0, 0)  # offset
        self.pos = vec(x, y)  # pixel

        self.rot = 0          # degree 0
        self.delta_rot = 0

        self.record = []
        self.power = ROBOT_POWER
        self.dirt = ROBOT_DIRT
        self.algorithm = ROBOT_ALGORITHM

        # for algorithm
        self.swalk_direction = 'L'
        self.swalk_distance = 0
        self.swalk_hitwall = 0
        self.swalk_order = 1

        self.mode = RobotMode.Manual
        self.state = RobotState.STOP
        self.rot_speed = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)

        keys = pg.key.get_pressed()
        if self.mode == RobotMode.Manual:
            if keys[pg.K_LEFT]:
                self.rot_speed = ROBOT_ROT_SPEED
            if keys[pg.K_RIGHT]:
                self.rot_speed = -ROBOT_ROT_SPEED
            if keys[pg.K_UP]:
                self.vel = vec(ROBOT_SPEED, 0).rotate(-self.rot)
            if keys[pg.K_DOWN]:
                self.vel = vec(-ROBOT_SPEED / 2, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        # record = []
        if self.mode == RobotMode.Auto:
            if self.algorithm == "RANDOM":
                self.algorithm_random()
            elif self.algorithm == "SWALK":
                self.algorithm_swalk()

            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.robot_img, self.rot)  # rotate image to new dir
            self.rect = self.image.get_rect()  # new rectangle
            self.rect.center = self.pos  # give new pos
            self.pos += self.vel * self.game.dt

            self.hit_rect.centerx = self.pos.x  # rotate along with center not corner and solve hit wall screen bouncing problem
            collide_with_walls(self, self.game.walls, 'x')  # ROBOT.hit_rect.centerx = sprite.pos.x
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')  # ROBOT.hit_rect.centery = sprite.pos.y
            self.rect.center = self.hit_rect.center
            self.record.append([self.pos])

        elif self.mode == RobotMode.Manual:
            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.robot_img, self.rot)  # rotate image to new dir
            self.rect = self.image.get_rect()  # new rectangle
            self.rect.center = self.pos  # give new pos
            self.pos += self.vel * self.game.dt

            self.hit_rect.centerx = self.pos.x  # rotate along with center not corner and solve hit wall screen bouncing problem
            collide_with_walls(self, self.game.walls, 'x')  # ROBOT.hit_rect.centerx = sprite.pos.x
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')  # ROBOT.hit_rect.centery = sprite.pos.y
            self.rect.center = self.hit_rect.center
            self.record.append([self.pos])

    def add_dirt(self, amount):
        self.dirt += amount
        if self.dirt > 100:
            self.dirt = 100

    def algorithm_random(self):
        """
                if hit rot random angle
                else just go
                """
        if self.state == RobotState.HITWALL:
            if random.randint(0, 1):
                self.rot_speed = random.randint(100, 1000) * 10
            else:
                self.rot_speed = -random.randint(100, 1000) * 10
            self.state = RobotState.RUNNING
        else:
            self.rot_speed = 0  # no rotation
            self.vel = vec(ROBOT_SPEED, 0).rotate(-self.rot)

    def algorithm_swalk(self):
        """
                if hit rotate 90 and go  and rotate 90 and go
                """
        if self.state == RobotState.HITWALL:
            self.delta_rot = 90
            self.swalk_distance = 15
            if self.swalk_order == 1:
                self.state = RobotState.SWALK_rot_1
            else:
                self.state = RobotState.SWALK_rot_2

            print('HITWALL', self.rot)
        elif self.state == RobotState.SWALK_rot_1 or self.state == RobotState.SWALK_rot_1_and_HITWALL:
            if self.state == RobotState.SWALK_rot_1_and_HITWALL:
                print('SWALK_rot_1_and_HITWALL')
            if self.swalk_direction == 'L':
                self.rot_speed = 150
            elif self.swalk_direction == 'R':
                self.rot_speed = -150

            new_rot = self.rot + self.rot_speed * self.game.dt

            self.delta_rot = self.delta_rot - math.fabs((new_rot - self.rot))
            if self.delta_rot < 0:
                if self.swalk_direction == 'L':
                    self.rot = self.rot + self.delta_rot
                    self.rot_speed = 0
                else:
                    self.rot = self.rot - self.delta_rot
                    self.rot_speed = 0

            if self.delta_rot < 0 or self.delta_rot == 0:
                if self.swalk_order == 1:
                    self.state = RobotState.SWALK_go_1_2
                else:
                    self.state = RobotState.RUNNING
                print('rot1done', self.rot)

        elif self.state == RobotState.SWALK_go_1_2 or self.state == RobotState.SWALK_and_HITWALL:

            if self.state == RobotState.SWALK_and_HITWALL:
                self.delta_rot += 90
                self.vel = vec(-100, 0).rotate(-self.rot)

                if self.swalk_order == 1:
                    self.state = RobotState.SWALK_rot_2
                else:
                    self.state = RobotState.SWALK_rot_1

                self.swalk_hitwall += 1
                if self.swalk_hitwall == 12:
                    self.swalk_hitwall = 0
                    self.delta_rot += 90
                    if random.randint(0,1):
                        self.swalk_order = 1
                    else:
                        self.swalk_order = 0

                else:
                    self.delta_rot = 90
                print('SWALK_and_HITWALL', self.swalk_hitwall)

                return

            self.vel = vec(ROBOT_SPEED, 0).rotate(-self.rot)

            self.swalk_distance -= 1
            print(self.swalk_distance)
            if self.swalk_distance == 0:
                self.swalk_hitwall = 0
                if self.swalk_order == 1:
                    self.state = RobotState.SWALK_rot_2
                else:
                    self.state = RobotState.SWALK_rot_1
                self.delta_rot = 90

        elif self.state == RobotState.SWALK_rot_2 or self.state == RobotState.SWALK_rot_2_and_HITWALL:
            if self.state == RobotState.SWALK_rot_2_and_HITWALL:
                print('SWALK_rot_2_and_HITWALL')
            if self.swalk_direction == 'L':
                self.rot_speed = 90
            elif self.swalk_direction == 'R':
                self.rot_speed = -90
            new_rot = self.rot + self.rot_speed * self.game.dt

            self.delta_rot = self.delta_rot - math.fabs((new_rot - self.rot))
            if self.delta_rot < 0:
                if self.swalk_direction == 'L':
                    self.rot = self.rot + self.delta_rot
                    self.rot_speed = 0
                else:
                    self.rot = self.rot - self.delta_rot
                    self.rot_speed = 0

            if self.delta_rot < 0 or self.delta_rot == 0:
                if self.swalk_order == 1:
                    self.state = RobotState.RUNNING
                else:
                    self.state = RobotState.SWALK_go_1_2
                if self.swalk_direction == 'L':
                    self.swalk_direction = 'R'
                elif self.swalk_direction == 'R':
                    self.swalk_direction = 'L'
                print('rot2done', self.rot)

        else:
            self.rot_speed = 0  # no rotation
            self.vel = vec(ROBOT_SPEED, 0).rotate(-self.rot)
            s = self.rot
            if self.rot > 290 or self.rot < 10:
                self.rot = 0
            elif self.rot > 80 and self.rot < 100:
                self.rot = 90
            elif self.rot > 170 and self.rot < 190:
                self.rot = 180
            elif self.rot > 260 and self.rot < 280:
                self.rot = 270





class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos
        self.hit_rect = ITEM_HIT_RECT
