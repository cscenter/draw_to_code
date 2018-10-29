from math import hypot


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
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def to_tex(self):
        return "\draw ({}, {}) -- ({}, {});".format(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y
        )

    def to_pil(self, draw):
        draw.line((self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y), fill=(255, 255, 255))


class Circle(Figure):
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius

    def to_tex(self):
        return "\draw ({}, {}) circle ({});".format(
            self.center.x,
            self.center.y,
            self.radius
        )

    def to_pil(self, draw):
        x = self.center.x
        y = self.center.y
        r = self.radius
        draw.arc([x - r, y - r, x + r, y + r], 0, 360, fill=(255, 255, 255))
