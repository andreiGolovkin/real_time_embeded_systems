from pygame_tools.Drawing_tools import *
from math import cos, sin, pi


class Shape:
    def __init__(self, *points):
        self.points = []

        for point in points:
            if isinstance(point, tuple):
                point = Point(point[0], point[1])

            self.points.append(point)

    def draw(self):
        circuit(*self.points)
        '''prev_index = -1
        for index in range(len(self.points)):
            p1 = self.points[prev_index]
            p2 = self.points[index]

            line(p1.x, p1.y, p2.x, p2.y, line_width=2)
            prev_index = index'''

    def get_walls(self):
        walls = []

        prev_index = -1
        for index in range(len(self.points)):
            p1 = self.points[prev_index]
            p2 = self.points[index]

            prev_index = index

            wall = (p1, p2)
            walls.append(wall)

        return walls

    @classmethod
    def circle(cls, center: Point, r: float, resolution: int = 100):
        circle_points = []
        for n in range(resolution):
            angle = 2 * pi * (n / resolution)
            point = Point(center.x + cos(angle) * r, center.y + sin(angle) * r)
            circle_points.append(point)

        circle = cls(*circle_points)

        return circle
