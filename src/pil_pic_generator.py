import os

from PIL import Image, ImageDraw

from geometry_generator import generate_triangle, generate_segment, generate_circle


PLOT_SIDE = 512
working_dir = "pics"

if not os.path.isdir(working_dir):
    os.mkdir(working_dir)

working_dir = os.path.join(os.getcwd(), working_dir)


def generate_pil_image(figures_list, plot_side=PLOT_SIDE):
    im = Image.new('RGBA', (plot_side, plot_side), (0, 255, 0, 0))
    draw = ImageDraw.Draw(im)
    for figure in figures_list:
        figure.to_pil(draw)
    return im


def save_pil_image(pil_image, path):
    pil_image.save(path + ".png")


for i in range(10):
    circle_1 = generate_circle(PLOT_SIDE)
    circle_2 = generate_circle(PLOT_SIDE)
    segment_1 = generate_segment(PLOT_SIDE)
    segment_2 = generate_segment(PLOT_SIDE)
    triangle = generate_triangle(PLOT_SIDE)
    figures = [circle_1, circle_2, segment_1, segment_2, *triangle]
    im = generate_pil_image(figures)
    save_pil_image(im, os.path.join(working_dir, "pic_{}".format(i)))
