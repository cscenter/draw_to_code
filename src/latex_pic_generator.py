import os

from geometry_generator import generate_triangle, generate_segment, generate_circle
from converter import TexConverter
from helper import save_as_png


TEMPLATE = """
\documentclass[border={{0 0 0 0}}]{{standalone}}
\\usepackage{{tikz}}


\\begin{{document}}
    {}
\end{{document}}
"""

PLOT_SIDE = 50


def convert_to_latex(figures):
    converter = TexConverter()
    fig = converter.convert(figures)
    return TEMPLATE.format(fig)


def convert_to_pic(figures, name, path):
    latex = convert_to_latex(figures)
    save_as_png(name, latex, path)


working_dir = "pics"

if not os.path.isdir(working_dir):
    os.mkdir("pics")

for i in range(1):
    circle_1 = generate_circle(PLOT_SIDE)
    circle_2 = generate_circle(PLOT_SIDE)
    segment_1 = generate_segment(PLOT_SIDE)
    segment_2 = generate_segment(PLOT_SIDE)
    triangle = generate_triangle(PLOT_SIDE)
    figures = [circle_1, circle_2, segment_1, segment_2, *triangle]
    convert_to_pic(figures, str(i), os.path.join(os.getcwd(), working_dir))

