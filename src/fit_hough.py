from random import choice, randint
import numpy as np
from PIL import ImageOps
from scipy.optimize import minimize

from hough import find_segments
import pic_generator
from geometry import Point, Segment, Line, Circle
from genetic import genetic, optimize_params
from pic_generator import load_figure_list


def segments_error(predictx, answerx, max_penalty):
    predict = list(filter(lambda x : isinstance(x, Segment), predictx))
    answer = list(filter(lambda x: isinstance(x, Segment), answerx))

    res = abs(len(predict) - len(answer))*max_penalty

    for p in predict:
        best = np.inf
        for a in answer:
            dist = Segment.difference(p, a)
            best = min(best, dist)
        res += min(best, max_penalty)

    for p in answer:
        best = np.inf
        for a in predict:
            dist = Segment.difference(p, a)
            best = min(best, dist)
        res += min(best, max_penalty)

    return res


def find_segments_fit(tests_in_epoch=10, max_penalty=1000):
    param_variants = [
        [10, 12, 15, 20, 30, 50, 70, 80, 100, 120, 150],  # min dist
        [0, 1, 2, 3, 5, 7, 10, 12, 15, 20, 25],  # min angle
        [0, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 70, 100],  # threshold hough
        [5, 10, 20, 30, 40],  # num peaks
        [180, 270, 360, 540, 720], # angles count
        [3, 5, 7, 10, 15, 20, 30, 40, 50, 70, 100],  # min seg len
        [1, 2, 3, 4, 5],  # window size
        [250, 500, 750, 1000, 1250]  # threshold seg
    ]

    fit_pics = [None] * tests_in_epoch
    fit_answers = [None] * tests_in_epoch
    for i in range(tests_in_epoch):
        in_image = pic_generator.load_image("../pics/bettertrain{}input.png".format(i))
        fit_pics[i] = np.array(ImageOps.invert(in_image))
        fit_answers[i] = load_figure_list("../pics/bettertrain{}answer.txt".format(i))

    def badness(params):
        error = 0
        for j in range(tests_in_epoch):
            predict = find_segments(fit_pics[j], *params)
            error += segments_error(predict, fit_answers[j], max_penalty)
        return error / tests_in_epoch

    res = optimize_params(param_variants, badness, crossing_chance=0.5)
    print(res[0], res[1])


if __name__ == "__main__":
    find_segments_fit()
