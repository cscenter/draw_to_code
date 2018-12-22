import os
import random

from PIL import Image, ImageChops, ImageDraw
import numpy as np

from geometry_generator import generate_triangle, generate_segment, generate_circle


def generate_pil_image(figures_list, image_side, background_color=255):
    im = Image.new('L', (image_side, image_side), background_color)
    draw = ImageDraw.Draw(im)
    for figure in figures_list:
        figure.to_pil(draw)
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
    threshold = 200
    return image.convert('L').point(lambda x : 255 if x > threshold else 0, mode='1')


def generate_random_pic(image_size, circles_amount=0, segments_amount=0, triangles_amount=0):
    figures = []

    for _ in range(circles_amount):
        figures.append(generate_circle(image_size))

    for _ in range(triangles_amount):
        figures.append(generate_triangle(image_size))

    for _ in range(segments_amount):
        figures.append(generate_segment(image_size))

    return generate_pil_image(figures, image_size), figures
