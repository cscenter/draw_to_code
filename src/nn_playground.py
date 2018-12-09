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
    y_list = []
    # y_is_fig_here_list = []

    for _ in range(pics_amount):
        im, figures = generate_random_pic(image_size, circles_amount, segments_amount)

        # is_fig_here = 0
        for figure in figures:
            if isinstance(figure, figure_class):
                y = figure.get_as_y(image_size)
                # is_fig_here = 1

        x_list.append(np.array(im))
        y_list.append(y)
        # y_is_fig_here_list.append(np.array([1]))

    X = np.array(x_list).reshape(pics_amount, image_size, image_size, 1)
    y = np.array(y_list)
    # y_is_fig_here = np.array(y_is_fig_here_list)

    return X, y, [1], figures


image_size = 100

X_train, y_train, y_is_fig_here, figures_train = generate_data(100, image_size, Circle, 1, 5)

model = get_circle_model(image_size)
model.fit(X_train, y_train, epochs=3)
# model.save_weights("get_circle.h5")
# print(np.shape(y_train))
# print(np.shape(y_is_fig_here))

# model = find_circle_model(image_size)
# model.fit(X_train, y_is_fig_here, epochs=3)
# model.save_weights("find_circle.h5")
