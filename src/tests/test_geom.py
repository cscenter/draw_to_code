import math

from geometry import Point, Line, Segment
from tests.testlib import check_eq, check_almost_eq


def test_line():
    l1 = Line(1, 0, 3) # x = 3
    l2 = Line(0, 2, 8) # y = 4
    l3 = Line(-1, 2, 1)

    p = Point(0, 3)
    check_almost_eq(l1.dist_to_point(p), 3.)
    check_almost_eq(l2.dist_to_point(p), 1.)
    check_almost_eq(l3.dist_to_point(p), math.sqrt(5.))


if __name__ == "__main__":
    test_line()