from math import atan2, hypot, pi, sin, cos, sqrt

import numpy as np
from sympy import Symbol, solve


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

    def __add__(self, other):
        assert isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Point)
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Point):
            return self.x*other.x + self.y*other.y
        else:
            return Point(self.x*other, self.y*other)

    def __str__(self):
        return "Point({}, {})".format(self.x, self.y)

    def norm(self):
        return self*(1/self.len())


class Segment(Figure):
    def __init__(self, point_1, point_2, color=0, width=0):
        self.width = width
        self.color = color
        self.point_1 = point_1
        self.point_2 = point_2

    def to_tex(self):
        s1 = "\\draw[line width=2pt] ({}, {}) -- ({}, {}); \n".format(
            round(self.point_1.y, 3),
            round(self.point_1.x, 3),
            round(self.point_2.y, 3),
            round(self.point_2.x,3)
        )
        s2 = "\\node[draw,circle,inner sep=2pt,fill] at ({}, {}) {{}}; \n".format(round(self.point_1.y,3), round(self.point_1.x, 3))
        s3 = "\\node[draw,circle,inner sep=2pt,fill] at ({}, {}) {{}}; \n\n".format(round(self.point_2.y, 3), round(self.point_2.x,3))
        return s1 + s2 + s3

    def to_pil(self, draw, width=0, color=0):
        xy = (self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y)
        draw.line(xy, fill=color, width=width)

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

    @staticmethod
    def difference(seg1, seg2):
        return min(
            Point.distance_between(seg1.point_1, seg2.point_1)**2 +
            Point.distance_between(seg1.point_2, seg2.point_2)**2,
            Point.distance_between(seg1.point_1, seg2.point_2)**2 +
            Point.distance_between(seg1.point_2, seg2.point_1)**2
        )

    def __str__(self):
        return "Segment(({}, {}), ({}, {}))".format(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y
        )


class Circle(Figure):
    def __init__(self, point, radius, color=0):
        self.color = color
        self.center = point
        self.radius = radius

    def to_tex(self):
        return "\\draw[line width=2pt] ({}, {}) circle ({}); \n".format(
            round(self.center.y,3),
            round(self.center.x, 3),
            round(self.radius, 3)
        )

    def to_pil(self, draw, width=0):
        x = self.center.x
        y = self.center.y
        r = self.radius
        draw.arc([x - r, y - r, x + r, y + r], 0, 360, fill=self.color, width=width)

    def get_as_y(self, image_size):
        y = np.array([
            self.center.x / image_size,
            self.center.y / image_size,
            self.radius / image_size * 2
        ])
        return y

    def project_point_seg(self, Seg : Segment, P : Point):
        ll = Line.line_by_two_points(Seg.point_1, Seg.point_2)
        #init_printing()
        x = Symbol('x')
        y = Symbol('y')
        sett = solve([(x - self.center.x) ** 2 + (y - self.center.y) ** 2 - self.radius**2, ll.a * x + ll.b * y - ll.c], [x, y])
        inters1_x = complex(sett[0][0]).real
        inters1_y = complex(sett[0][1]).real
        inters2_x = complex(sett[1][0]).real
        inters2_y = complex(sett[1][1]).real
        dist1 = Point.distance_between(Point(inters1_x, inters1_y), P)
        dist2 = Point.distance_between(Point(inters2_x, inters2_y), P)
        if dist1 < dist2:
            return Point(inters1_x, inters1_y)
        return Point(inters2_x, inters2_y)

    @staticmethod
    def construct_from_y(y, image_size):
        return Circle(
            Point(
                y[0] * image_size,
                y[1] * image_size
            ),
            y[2] * image_size / 2
        )


def angle(p : Point):  # angle between p and OX
    if p.x > 0:
        return np.arctan(p.y / p.x)
    if p.x < 0:
        return angle(Point(-p.x, -p.y)) + np.pi
    if p.x == 0:
        return np.pi/2 if p.y >= 0 else -np.pi/2


class Line(Figure):
    # ax + by = c
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return "Line({}, {}, {})".format(self.a, self.b, self.c)

    @staticmethod
    def cross(l1, l2):
        if l1.a*l2.b == l2.a*l1.b:
            return None
        else:
            return Point(
                (l1.c*l2.b - l2.c*l1.b) / (l1.a*l2.b - l2.a*l1.b),
                (l1.c*l2.a - l2.c*l1.a) / (l1.b*l2.a - l2.b*l1.a)
            )

    def dist_to_point(self, point : Point):
        a, b, c = self.a, self.b, self.c
        x, y = point.x, point.y
        return abs(a*x + b*y - c)/np.sqrt(a*a + b*b)

    @staticmethod
    def line_by_ro_theta(ro, theta):
        return Line(np.sin(theta), np.cos(theta), ro)
    
    @staticmethod
    def line_by_ro_theta_1(ro, theta):
        return Line(np.cos(theta), np.sin(theta), ro)

    @staticmethod
    def line_by_two_points(p1 : Point, p2 : Point):
        dir = Point(p2.x - p1.x, p2.y - p1.y)
        a, b = -dir.y, dir.x
        c = a*p1.x + b*p1.y
        return Line(a, b, c)

    def ro(self):
        return self.dist_to_point(Point(0, 0))

    def theta(self):
        p = Line.cross(self, Line(-self.b, self.a, 0))
        return angle(p)

    def to_pil(self, draw, img_size, color=0):
        if abs(self.a) > abs(self.b): #more horisontal line
            left = Line(0, 1, 0)
            right = Line(0, 1, img_size)
            p1 = Line.cross(self, left)
            p2 = Line.cross(self, right)
        else:  # more vertical line
            down = Line(1, 0, 0)
            up = Line(1, 0, img_size)
            p1 = Line.cross(self, down)
            p2 = Line.cross(self, up)
        Segment(p1, p2, color=color).to_pil(draw)

        
    def is_similar(self, line2):
        an = self.a / sqrt(self.a ** 2 + self.b ** 2)
        bn = self.b / sqrt(self.a ** 2 + self.b ** 2)
        cn = self.c / sqrt(self.a ** 2 + self.b ** 2)
        an2 = line2.a / sqrt(line2.a ** 2 + line2.b ** 2)
        bn2 = line2.b / sqrt(line2.a ** 2 + line2.b ** 2)
        cn2 = line2.c / sqrt(line2.a ** 2 + line2.b ** 2)
        dett = an * bn2 - an2 * bn
        thr_det = 0.1#0.05
        thr_c = 8#5
        is_par = (abs(dett) < thr_det)
        if not is_par:
            return False
        if cn * cn2 < 0:
            cn2 *= -1
        return (abs(cn - cn2) < thr_c)

    def cross_with_rect(self, p1 : Point, p2 : Point, eps=0.001):
        x1, y1, x2, y2 = p1.x, p1.y, p2.x, p2.y
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        sides = [Line(1, 0, x1), Line(0, 1, y1),
                 Line(1, 0, x2), Line(0, 1, y2)]
        good_points = []
        for side in sides:
            point = Line.cross(self, side)
            if point is not None and\
                    x1 - eps <= point.x <= x2 + eps and\
                    y1 - eps <= point.y <= y2 + eps:
                good_points.append(point)

        if len(good_points) == 0:
            return None

        start_point = good_points[0]
        end_point = None
        for point in good_points:
            if (start_point - point).len() > eps:
                end_point = point
                break

        if end_point is None:
            return None
        else:
            return Segment(start_point, end_point)

    def find_project(self, p : Point):
        anorm = self.a / sqrt(self.a ** 2 + self.b ** 2)
        bnorm = self.b / sqrt(self.a ** 2 + self.b ** 2)
        dist = self.dist_to_point(p)
        movex = anorm * dist
        movey = bnorm * dist
        v1x = p.x + movex
        v1y = p.y + movey
        v2x = p.x - movex
        v2y = p.y - movey
        diff1 = abs(self.a * v1x + self.b * v1y - self.c)
        diff2 = abs(self.a * v2x + self.b * v2y - self.c)
        if diff1 < diff2:
            return Point(v1x, v1y)
        return Point(v2x, v2y)

