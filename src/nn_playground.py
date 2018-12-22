from random import randint, uniform

import keras
import keras.layers as L

import numpy as np

from geometry_generator import generate_circle, generate_segment
from geometry import Circle, Point, Segment
from pic_generator import generate_random_pic, save_pil_image, generate_pil_image, add_noise

from models.circle import find_circle_model, get_circle_model
from models.segment import find_segment_model, get_segment_model


def generate_data(pics_amount, image_size, figure_class, fix_circle=False, fix_segment=False):
    x_list = []
    y_list = []
    y_is_fig_here_list = []

    for _ in range(pics_amount):
        circles_amount = 1 if fix_circle else randint(0, 3)
        segments_amount = 1 if fix_segment else randint(0, 5)
        im, figures = generate_random_pic(image_size, circles_amount, segments_amount)
        im = add_noise(im, uniform(0, 0.07))

        is_fig_here = 0
        y = None
        for figure in figures:
            if isinstance(figure, figure_class):
                y = figure.get_as_y(image_size)
                is_fig_here = 1

        x_list.append(np.array(im))
        y_list.append(y)
        y_is_fig_here_list.append(np.array(is_fig_here))

    X = np.array(x_list).reshape(pics_amount, image_size, image_size, 1)
    y = np.array(y_list)
    y_is_fig_here = np.array(y_is_fig_here_list)

    return X, y, y_is_fig_here


def fit_model(train_model, image_amount=500000, epochs=3, image_size=100):
    fix_circle = False
    fix_segment = False

    if train_model == "get_segment_model":
        model = get_segment_model(image_size)
        train_fig = Segment
        fix_segment = True

    if train_model == "get_circle_model":
        model = get_circle_model(image_size)
        train_fig = Circle
        fix_circle = True

    if train_model == "find_segment_model":
        model = find_segment_model(image_size)
        train_fig = Segment

    if train_model == "find_circle_model":
        model = find_circle_model(image_size)
        train_fig = Circle

    X_train, y_train, y_is_fig_here = generate_data(image_amount, image_size, train_fig, fix_circle, fix_segment)

    if train_model.startswith("get"):
        model.fit(X_train, y_train, epochs=epochs)
    elif train_model.startswith("find"):
        model.fit(X_train, y_is_fig_here, epochs=epochs)

    model.save_weights("{}.h5".format(train_model))


train_models = ["get_segment_model", "get_circle_model", "find_segment_model", "find_circle_model"]
for model in train_models:
    fit_model(model)
