import os
from random import uniform

from geometry import *
from converter import TexConverter
from helper import save_as_png


TEMPLATE = """
\documentclass[border={{0 0 0 0}}]{{standalone}}
\\usepackage{{tikz}}


\\begin{{document}}
    {}
\end{{document}}
"""


def convert_to_latex(figures):
    converter = TexConverter()
    fig = converter.convert(figures)
    return TEMPLATE.format(fig)


def convert_to_pic(figures, name, path):
    latex = convert_to_latex(figures)
    save_as_png(name, latex, path)


def generate_circle(plot_side=50):
    radius = uniform(plot_side / 10, plot_side / 2)
    x = uniform(radius, plot_side - radius)
    y = uniform(radius, plot_side - radius)
    center = Point(x, y)
    return Circle(center, 5)


def generate_segment(plot_side=50):
    point_1 = Point(uniform(0, plot_side), uniform(0, plot_side))
    point_2 = Point(uniform(0, plot_side), uniform(0, plot_side))
    return Segment(point_1, point_2)


working_dir = "pics"

if not os.path.isdir(working_dir):
    os.mkdir("pics")

for i in range(1):
    circle_1 = generate_circle()
    circle_2 = generate_circle()
    segment_1 = generate_segment()
    segment_2 = generate_segment()
    figures = [circle_1, circle_2, segment_1, segment_2]
    convert_to_pic(figures, str(i), os.path.join(os.getcwd(), working_dir))

