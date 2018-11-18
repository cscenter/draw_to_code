from math import atan2, hypot, pi, sin, cos


class Figure:
    def to_tex(self):
        raise NotImplementedError


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance_between(p1, p2):
        return hypot(p1.x - p2.x, p1.y - p2.y)


class Segment(Figure):
    def __init__(self, point_1, point_2, color=None, width=0):
        self.width = width
        self.color = color or 0
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
    def segment_by_point_angle_length(point, angle, length, color=None, width=0):
        d_x = length / 2 * cos(angle)
        d_y = length / 2 * sin(angle)
        point_1 = Point(point.x - d_x, point.y - d_y)
        point_2 = Point(point.x + d_x, point.y + d_y)
        return Segment(point_1, point_2, color, width)


class Circle(Figure):
    def __init__(self, point, radius, color=None):
        self.color = color or 0
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
