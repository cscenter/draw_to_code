import os
import random

from PIL import Image, ImageChops, ImageDraw
import numpy as np
from random import randint

from geometry_generator import generate_triangle, generate_segment, generate_circle
from latex_pic_generator import convert_to_pic
from geometry import Point, Segment, Circle, Line


def generate_pil_image(figures_list, image_side, background_color=255, width=0):
    im = Image.new('L', (image_side, image_side), background_color)
    draw = ImageDraw.Draw(im)
    for figure in figures_list:
        figure.to_pil(draw, width=width)
    return im


def add_noise(im, threshold=0.05):
    arr = np.array(im)
    mask = np.random.rand(*arr.shape)
    arr[mask < threshold] = 0
    arr[mask > 1 - threshold] = 255
    return Image.fromarray(arr)


def subtract_image(image1, image2):
    return ImageChops.lighter(image1, ImageChops.invert(image2))


def save_pil_image(pil_image, path):
    pil_image.save(path + ".png")


def load_image(image_path):
    image = Image.open(image_path)
    threshold = 180
    return image.convert('L').point(lambda x : 255 if x > threshold else 0)


def image_to_square(image, size, background_color=255):
    image_size = image.size
    width = image_size[0]
    height = image_size[1]

    bigside = width if width > height else height

    background = Image.new('L', (bigside, bigside), background_color)
    offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2), 0)))

    background.paste(image, offset)
    return background.resize((size, size))


def generate_random_pic(image_size,
                        circles_amount=0, segments_amount=0, triangles_amount=0,
                        figures_width=0):
    figures = []

    for _ in range(circles_amount):
        figures.append(generate_circle(image_size))

    for _ in range(triangles_amount):
        figures += list(generate_triangle(image_size))

    for _ in range(segments_amount):
        figures.append(generate_segment(image_size))

    return generate_pil_image(figures, image_size, width=figures_width), figures


def save_figures(figures, filepath):
    fout = open(filepath, "w")

    for fig in figures:
        if isinstance(fig, Segment):
            p1, p2 = fig.point_1, fig.point_2
            fout.write('segment {} {} {} {}\n'.format(p1.x, p1.y, p2.x, p2.y))
        elif isinstance(fig, Circle):
            fout.write('circle {} {} {}\n'.format(fig.radius, fig.center.x, fig.center.y))
        else:
            raise RuntimeError("Can't save {} object".format(type(fig)))

    fout.close()


def load_figure_list(filepath):
    f = open(filepath, "r")
    res = []
    for s in f.readlines():
        words = s.split()
        nums = list(map(float, words[1:]))
        t = words[0]

        if t == 'segment':
            res.append(Segment(
                Point(nums[0], nums[1]),
                Point(nums[2], nums[3])
            ))
        elif t == 'circle':
            res.append(Circle(
                Point(nums[1], nums[2]),
                nums[0]
            ))
        else:
            raise RuntimeError("Can't load figure named {}".format(t))

    f.close()
    return res


def generate_dataset(image_size, amount, filename,
                     max_segments=5, max_circles=5, max_triangles=3,
                     fig_width=0):
    for i in range(amount):
        pic, fig = generate_random_pic(image_size,
                                       segments_amount=randint(0, max_segments),
                                       circles_amount=randint(0, max_circles),
                                       triangles_amount=randint(0, max_triangles),
                                       figures_width=fig_width)
        save_figures(fig, "{}{}answer.txt".format(filename, i))
        pic.save("{}{}input.png".format(filename, i))


if __name__ == "__main__":
    generate_dataset(500, 10, "../pics/bettertrain", fig_width=2,
                     max_segments=3, max_circles=2, max_triangles=1)
