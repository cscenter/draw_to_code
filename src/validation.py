from random import randint

from geometry_generator import generate_circle, generate_segment, generate_triangle
from pil_pic_generator import generate_pil_image


IMAGE_SIZE = 32


def generate_pic():
    circles_amount = randint(0, 3)
    triangles_amount = randint(0, 3)
    segments_amount = randint(0, 3)

    figures = []

    for _ in range(circles_amount):
        figures.append(generate_circle(IMAGE_SIZE))

    for _ in range(triangles_amount):
        figures.append(generate_triangle(IMAGE_SIZE))

    for _ in range(segments_amount):
        figures.append(generate_segment(IMAGE_SIZE))

    return generate_pil_image(figures), figures


def get_data(size):
    return [generate_pic() for _ in range(size)]


def run_test(find_circle_model, get_circle_model, find_segment_model, get_segment_model):
    data = get_data(1000)
    

