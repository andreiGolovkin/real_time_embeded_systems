from pygame_tools.Drawing_tools import *
from pygame_tools.Geometry.Transform import Transform
from Shape import Shape
from math import cos, sin, pi
from Robot import Robot
from Ray import Ray
import time


if __name__ == "__main__":
    set_win_size(1400, 800)

    cones = []

    r = 70
    num_cones = 8
    angle_offset = pi / 4
    center = Point(520, 400)
    for n in range(num_cones):
        angle = 2 * pi * (n / num_cones) + angle_offset
        direction = Point(cos(angle), sin(angle))
        cone = Shape.circle(center + direction * r, 10, resolution=10)

        cones.append(cone)

    r = 200
    angle_scale = 78 / 100
    num_cones = 12
    angle_offset = angle_scale
    center = Point(520, 400)
    for n in range(num_cones + 1):
        angle = (2 * pi) * angle_scale * (n / num_cones) + angle_offset
        direction = Point(cos(angle), sin(angle))
        cone = Shape.circle(center + direction * r, 10, resolution=10)

        cones.append(cone)

    r = 70
    num_cones = 8
    angle_offset = pi / 4
    center = Point(880, 400)
    for n in range(num_cones):
        angle = 2 * pi * (n / num_cones) + angle_offset
        direction = Point(cos(angle), sin(angle))
        cone = Shape.circle(center + direction * r, 10, resolution=10)

        cones.append(cone)

    r = 200
    angle_scale = 78/100
    num_cones = 12
    angle_offset = -pi*angle_scale
    center = Point(880, 400)
    for n in range(num_cones+1):
        angle = (2 * pi) * angle_scale * (n / num_cones) + angle_offset
        direction = Point(cos(angle), sin(angle))
        cone = Shape.circle(center + direction * r, 10, resolution=10)

        cones.append(cone)

    robot = Robot(880 + 135, screen_height() / 2, pi/2)

    robot.forward(5)

    mouse = get_mouse()
    game_finished = False
    while not game_finished:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_finished = True

        robot.update(*cones)

        if robot.right_sensor.length < 50:
            robot.left(10)
        elif robot.left_sensor.length < 50:
            robot.right(10)
        else:
            robot.left(0)

        background(BLACK)

        for cone in cones:
            cone.draw()

        robot.draw()

        update_display()
