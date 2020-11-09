from pygame_tools.Geometry.Point import Point
from pygame_tools.Geometry.Transform import Transform
from pygame_tools.Geometry import to_point

from Shape import Shape


class Ray:
    def __init__(self, x, y, angle):
        self.orig_offset = Transform(x, y, angle)

        self.max_ray_dist = 300
        self.length = self.max_ray_dist

    def update(self, robot_pos: Transform, *shapes):
        ray_origin, ray_dir = self.get_orig_point_and_dir(robot_pos)

        self.length = self.max_ray_dist
        for shape in shapes:
            self.get_intersection_with_shape(ray_origin, ray_dir, shape)

    def get_intersection_with_shape(self, ray_origin: Point, ray_dir: Point, shape: Shape):

        walls = shape.get_walls()

        for wall in walls:
            p11 = ray_origin
            p12 = ray_origin + ray_dir

            p21 = wall[0]
            p22 = wall[1]

            intersection = self.get_intersection(p11, p12, p21, p22)

            if intersection["is_intersects"]:
                intersection_point = intersection["intersection_point"]

                dist_to_intersection = ray_origin.dist(intersection_point)

                if dist_to_intersection < self.length:
                    self.length = dist_to_intersection

    def get_orig_point_and_dir(self, robot_pos: Transform):
        ray_origin = robot_pos.with_offset_t(self.orig_offset)
        ray_dir = ray_origin.with_offset(1)

        ray_origin = to_point(ray_origin)
        ray_dir = to_point(ray_dir) - ray_origin

        return ray_origin, ray_dir

    @classmethod
    def get_intersection(cls, p11: Point, p12: Point, p21: Point, p22: Point):
        intersection = {"is_intersects": False, "intersection_point": None}

        x1 = p11.x
        y1 = p11.y
        x2 = p12.x
        y2 = p12.y

        x3 = p21.x
        y3 = p21.y
        x4 = p22.x
        y4 = p22.y

        div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if div != 0:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / div
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / div

            if t >= 0 and 0 <= u <= 1:
                px = x1 + t * (x2 - x1)
                py = y1 + t * (y2 - y1)

                intersection["is_intersects"] = True
                intersection["intersection_point"] = Point(px, py)

        return intersection
