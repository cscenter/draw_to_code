from random import uniform

from geometry import Circle, Point, Segment


def generate_circle(plot_side):
    radius = uniform(plot_side / 10, plot_side / 2)
    x = uniform(radius, plot_side - radius)
    y = uniform(radius, plot_side - radius)
    center = Point(x, y)
    return Circle(center, radius)


def generate_segment(plot_side):
    min_segment = plot_side / 10
    point_1 = Point(uniform(0, plot_side), uniform(0, plot_side))
    while True:
        point_2 = Point(uniform(0, plot_side), uniform(0, plot_side))
        if Point.distance_between(point_1, point_2) > min_segment:
            break
    return Segment(point_1, point_2)


def generate_triangle(plot_side):
    min_segment = plot_side / 10
    point_1 = Point(uniform(0, plot_side), uniform(0, plot_side))
    while True:
        point_2 = Point(uniform(0, plot_side), uniform(0, plot_side))
        if Point.distance_between(point_1, point_2) > min_segment:
            break
    while True:
        point_3 = Point(uniform(0, plot_side), uniform(0, plot_side))
        if min(Point.distance_between(point_1, point_3), Point.distance_between(point_2, point_3)) > min_segment:
            break
    segment_1 = Segment(point_1, point_2)
    segment_2 = Segment(point_1, point_3)
    segment_3 = Segment(point_2, point_3)
    return segment_1, segment_2, segment_3
