import os

from geometry_generator import generate_triangle, generate_segment, generate_circle
from converter import TexConverter
from helper import save_as_png


TEMPLATE = """
\documentclass[12pt, a4paper]{{standalone}}
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
