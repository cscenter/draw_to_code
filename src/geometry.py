from math import atan2, hypot, pi, sin, cos

import numpy as np


class Figure:
    def to_tex(self):
        raise NotImplementedError

    def to_pil(self):
        raise NotImplementedError

    def get_as_y(self, image_size):
        raise NotImplementedError


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance_between(p1, p2):
        return hypot(p1.x - p2.x, p1.y - p2.y)

    def len(self):
        return Point.distance_between(self, Point(0, 0))


class Segment(Figure):
    def __init__(self, point_1, point_2, color=0, width=0):
        self.width = width
        self.color = color
        self.point_1 = point_1
        self.point_2 = point_2

    def to_tex(self):
        return "\\draw ({}, {}) -- ({}, {});".format(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y
        )

    def to_pil(self, draw):
        xy = (self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y)
        draw.line(xy, fill=self.color, width=self.width)

    def get_middle(self):
        x = (self.point_1.x + self.point_2.x) / 2
        y = (self.point_1.y + self.point_2.y) / 2
        return Point(x, y)

    def get_angle(self):
        angle = atan2(self.point_2.y - self.point_1.y, self.point_2.x - self.point_1.x)
        if angle < 0:
            angle += pi
        return angle

    def get_length(self):
        return Point.distance_between(self.point_1, self.point_2)

    @staticmethod
    def segment_by_point_angle_length(point, angle, length, color=0, width=0):
        d_x = length / 2 * cos(angle)
        d_y = length / 2 * sin(angle)
        point_1 = Point(point.x - d_x, point.y - d_y)
        point_2 = Point(point.x + d_x, point.y + d_y)
        return Segment(point_1, point_2, color, width)

    def get_as_y(self, image_size):
        middle_point = self.get_middle()
        y = np.array([middle_point.x, middle_point.y, self.get_angle(), self.get_length()])
        y[0] /= image_size
        y[1] /= image_size
        y[3] /= (image_size * 1.4)  # sqrt(2)
        return y

    @staticmethod
    def construct_from_y(y, image_size):
        y[0] *= image_size
        y[1] *= image_size
        y[3] *= (image_size * 1.4)  # sqrt(2)
        point = Point(y[0], y[1])
        return Segment.segment_by_point_angle_length(point, y[2], y[3])


class Circle(Figure):
    def __init__(self, point, radius, color=0):
        self.color = color
        self.center = point
        self.radius = radius

    def to_tex(self):
        return "\\draw ({}, {}) circle ({});".format(
            self.center.x,
            self.center.y,
            self.radius
        )

    def to_pil(self, draw):
        x = self.center.x
        y = self.center.y
        r = self.radius
        draw.arc([x - r, y - r, x + r, y + r], 0, 360, fill=self.color)

    def get_as_y(self, image_size):
        y = np.array([
            self.center.x / image_size,
            self.center.y / image_size,
            self.radius / image_size * 2
        ])
        return y

    @staticmethod
    def construct_from_y(y, image_size):
        return Circle(
            Point(
                y[0] * image_size,
                y[1] * image_size
            ),
            y[2] * image_size / 2
        )


class Line(Figure):
    # ax + by = c
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


    @staticmethod
    def cross(l1, l2):
        if l1.a*l2.b == l2.a*l1.b:
            return None
        else:
            return Point(
                (l1.c*l2.a - l2.c*l1.a) / (l1.b*l2.a - l2.b*l1.a),
                (l1.c*l2.b - l2.c*l1.b) / (l1.a*l2.b - l2.a*l1.b)
            )

    def dist_to_point(self, point):
        x, y = point.x, point.y
        a, b, c = self.a, self.b, self.c
        return abs(a*(x - c/a) + b*y)/np.sqrt(a*a + b*b)

    @staticmethod
    def line_by_ro_theta(ro, theta):
        return Line(np.cos(theta), np.sin(theta), ro)

    def ro(self):
        return self.dist_to_point(Point(0, 0))

    def theta(self):
        return np.arctan(self.b / self.a)

    def to_pil(self, draw, img_size, color=0):
        if abs(self.a) < abs(self.b): #more horisontal line
            left = Line(0, 1, 0)
            right = Line(0, 1, img_size)
            p1 = Line.cross(self, left)
            p2 = Line.cross(self, right)
        else: # more vertical line
            down = Line(1, 0, 0)
            up = Line(1, 0, img_size)
            p1 = Line.cross(self, down)
            p2 = Line.cross(self, up)
        Segment(p1, p2, color=color).to_pil(draw)



