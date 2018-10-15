class Figure:
    def to_tex(self):
        raise NotImplementedError


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
