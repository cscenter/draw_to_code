import numpy as np

from geometry import Point, Line, Segment
from tests.testlib import check_eq, check_almost_eq, TestNotPassed
from random import uniform


def check_eq_points(p1 : Point, p2 : Point):
    check_almost_eq(p1.x, p2.x)
    check_almost_eq(p1.y, p2.y)


def check_eq_lines(l1 : Line, l2 : Line):
    if abs(l1.a) > abs(l1.b):
        koef = l1.a / l2.a
    else:
        koef = l1.b / l2.b
    try:
        check_almost_eq(l1.a, l2.a * koef)
        check_almost_eq(l1.b, l2.b * koef)
        check_almost_eq(l1.c, l2.c * koef)
    except TestNotPassed:
        print("Line 1:", l1.a, l1.b, l1.c)
        print("Line 2:", l2.a, l2.b, l2.c)
        raise TestNotPassed



def test_line():
    l1 = Line(1, 0, 3) # x = 3
    l2 = Line(0, 2, 8) # y = 4
    l3 = Line(-1, 2, 1)

    p = Point(0, 3)
    check_almost_eq(l1.dist_to_point(p), 3.)
    check_almost_eq(l2.dist_to_point(p), 1.)
    check_almost_eq(l3.dist_to_point(p), np.sqrt(5.))

    check_eq_points(Line.cross(l1, l2), Point(3, 4))
    check_eq_points(Line.cross(l1, l3), Point(3, 2))
    check_eq_points(Line.cross(l2, l3), Point(7, 4))

    abc1 = Line(3, 2, 13)
    roth1 = Line.line_by_ro_theta(np.sqrt(13), np.arctan(2/3))
    abc2 = Line(1, 0, 5)
    roth2 = Line.line_by_ro_theta(5, 0)
    abc3 = Line(0, 1, 5)
    roth3 = Line.line_by_ro_theta(5, np.pi/2)
    abc4 = Line(0, 1, -7)
    roth4 = Line.line_by_ro_theta(7, -np.pi/2)
    check_eq_lines(abc1, roth1)
    check_eq_lines(abc2, roth2)
    check_eq_lines(abc3, roth3)
    check_eq_lines(abc4, roth4)

    for _ in range(100000):
        a, b,c = 0, 0, 0
        while abs(a) + abs(b) < 0.000001:
            a, b, c = [uniform(-100, 100) for _ in range(3)]
        l1 = Line(a, b, c)
        ro, theta = l1.ro(), l1.theta()
        l2 = Line.line_by_ro_theta(ro, theta)
        check_eq_lines(l1, l2)




if __name__ == "__main__":
    test_line()
