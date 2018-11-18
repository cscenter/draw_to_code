import os

from PIL import Image, ImageChops, ImageDraw

from geometry_generator import generate_triangle, generate_segment, generate_circle


def generate_pil_image(figures_list, image_side, background_color=256):
    im = Image.new('L', (image_side, image_side), background_color)
    draw = ImageDraw.Draw(im)
    for figure in figures_list:
        figure.to_pil(draw)
    return im


def subtract_image(image1, image2):
    return ImageChops.add(image1, image2)


def save_pil_image(pil_image, path):
    pil_image.save(path + ".png")


def generate_random_pic(image_size, circles_amount, segments_amount, triangles_amount):
    figures = []

    for _ in range(circles_amount):
        figures.append(generate_circle(image_size))

    for _ in range(triangles_amount):
        figures.append(generate_triangle(image_size))

    for _ in range(segments_amount):
        figures.append(generate_segment(image_size))

    return generate_pil_image(figures, image_size), figures
