import keras
import keras.layers as L

import numpy as np

from geometry_generator import generate_circle, generate_segment
from geometry import Circle, Point, Segment
from pic_generator import generate_random_pic, save_pil_image, generate_pil_image

from models.circle import find_circle_model, get_circle_model
from models.segment import find_segment_model, get_segment_model


def generate_data(pics_amount, image_size, figure_class, circles_amount, segments_amount):
    x_list = []
    y_list  = []

    for _ in range(pics_amount):
        im, figures = generate_random_pic(image_size, circles_amount, segments_amount)

        for figure in figures:
            if isinstance(figure, figure_class):
                y = figure.get_as_y(image_size)

        x_list.append(np.array(im))
        y_list.append(y)

    X = np.array(x_list).reshape(pics_amount, image_size, image_size, 1)
    y = np.array(y_list)

    return X, y, figures


image_size = 100
model = get_circle_model(image_size)
model.load_weights("get_circle.h5")

for i in range(10):
    X_test, y_test, figures_test = generate_data(1, image_size, Circle, 1, 5)

    res = model.predict(X_test)
    res = res[0]
    # res = [res[0], res[1], res[3]]
    segment = Circle.construct_from_y(res, image_size)
    segment.color = 128

    result_im = generate_pil_image(figures_test + [segment], image_size)
    save_pil_image(result_im, "pics/test_{}".format(i))
