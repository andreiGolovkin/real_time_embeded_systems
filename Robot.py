from pygame_tools.Geometry.Transform import Transform
from pygame_tools.Drawing_tools import *
from math import cos, sin, pi
from Ray import Ray


class Robot(Transform):
    def __init__(self, x=0, y=0, theta=0):
        super(Robot, self).__init__(x, y, theta)

        self.r = 10

        sensor_angle = pi * (1/3)
        x = cos(sensor_angle) * self.r
        y = sin(sensor_angle) * self.r
        self.right_sensor = Ray(x, y, sensor_angle)

        x = cos(-sensor_angle) * self.r
        y = sin(-sensor_angle) * self.r
        self.left_sensor = Ray(x, y, -sensor_angle)

        self.steering_level = 0
        self.speed_level = 0

        self.steering_dir = 1
        self.dir = 1

        self.max_steering_angle = pi / 6
        self.max_speed = 5

        self.max_steering_level = 20
        self.max_speed_level = 20

    def forward(self, level: int):
        self.set_speed_level(level)
        self.dir = 1

    def backward(self, level: int):
        self.set_speed_level(level)
        self.dir = -1

    def left(self, level: int):
        self.set_steering_level(level)
        self.steering_dir = -1

    def right(self, level: int):
        self.set_steering_level(level)
        self.steering_dir = 1

    def set_steering_level(self, level: int):
        if 0 <= level <= self.max_steering_level:
            self.steering_level = level
        elif level < 0:
            self.steering_level = 0
        elif level > self.max_steering_level:
            self.steering_level = self.max_steering_level

    def set_speed_level(self, level: int):
        if 0 <= level <= self.max_speed_level:
            self.speed_level = level
        elif level < 0:
            self.speed_level = 0
        elif level > self.max_speed_level:
            self.speed_level = self.max_speed_level

    def update(self, *shapes):
        self.move()

        self.right_sensor.update(self, *shapes)
        self.left_sensor.update(self, *shapes)

    def move(self):
        speed = self.max_speed * (self.speed_level / self.max_speed_level) * self.dir
        angle = self.max_steering_angle * (self.steering_level / self.max_steering_level) *\
                (self.steering_dir if self.dir > 0 else -self.steering_dir)
        self.add(x_offset=speed, theta_offset=angle)

    def draw(self):
        color(RED)
        ray_origin, ray_dir = self.right_sensor.get_orig_point_and_dir(self)
        line(*ray_origin.as_tuple(), *(ray_origin + ray_dir * self.right_sensor.length).as_tuple())

        ray_origin, ray_dir = self.left_sensor.get_orig_point_and_dir(self)
        line(*ray_origin.as_tuple(), *(ray_origin + ray_dir * self.left_sensor.length).as_tuple())

        x, y, angle = self.to_xya()

        color(WHITE)
        ellipse(x, y, 2 * self.r, 2 * self.r, fill=False)
        line(x + cos(angle) * 5, y + sin(angle) * 5, x + cos(angle) * 13, y + sin(angle) * 13)
