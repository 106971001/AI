from enum import Enum
from sprite.Sensor import SensorType
from random import randint

class RandomAlgorithmAction(Enum):
    WALK = 1
    ROTATE = 2


class RandomAlgorithm:

    def __init__(self):
        self.name = "RandomAlgorithm"
        self.started = False
        self.min_threshold_walk = 5

    def update(self, sensors):
        walk = True
        rotate = False

        # check if any laser distance lower than threshold
        for sensor in sensors:
            if sensor.type == SensorType.Laser:
                if sensor.value[0] < self.min_threshold_walk:
                    walk = False
                    rotate = True
                elif sensor.name == "left_laser" or sensor.name == "right_laser":
                    if sensor.value[0] < self.min_threshold_walk*2:
                        walk = False
                        rotate = True
            if not walk:
                break

        # if not walk than rotate
        if walk:
            return RandomAlgorithmAction.WALK, 0
        elif rotate:
            delta_angle = randint(70, 150)
            if randint(0,1):
                delta_angle = delta_angle * -1
            return RandomAlgorithmAction.ROTATE, delta_angle

    def start(self):
        self.started = True
