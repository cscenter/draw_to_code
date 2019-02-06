from random import choice, randint
import numpy as np

from hough import find_segments
import pic_generator
from geometry import Point, Segment, Line, Circle
from PIL import ImageOps


def segments_error(predict, answer, max_penalty):
    res = 0

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


def load_segments_list(filepath):
    f = open(filepath, "r")
    res = []
    for s in f.readlines():
        x1, y1, x2, y2 = list(map(int, s.split()))
        res.append(Segment(
            Point(x1, y1),
            Point(x2, y2)
        ))
    f.close()
    return res


def find_segments_fit(epochs, tests_in_epoch, max_penalty=100):
    params_variants = [
        [0, 1, 2, 3, 5, 7, 10, 12, 15, 20, 30], # min dist
        [0, 1, 2, 3, 5, 7, 10, 12, 15, 20, 25], # min angle
        [0, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 70, 100], # threshold hough
        [5, 10, 20, 30, 40], # num peaks
        [3, 5, 7, 10, 15, 20, 30, 40, 50, 70, 100], # min seg len
        [0, 1, 2, 3], # window size
        [200, 300, 400, 500, 800, 1000, 1500] # threshold seg
    ]

    fit_pics = [None]*tests_in_epoch
    fit_answers = [None]*tests_in_epoch
    for i in range(tests_in_epoch):
        in_image = pic_generator.load_image("../pics/train{}.bmp".format(i))
        fit_pics[i] = np.array(ImageOps.invert(in_image))
        fit_answers[i] = load_segments_list("../pics/ans{}.txt".format(i))

    best_error = np.inf
    best_params = None
    for i in range(epochs):
        params = [choice(vars) for vars in params_variants]
        error = 0
        for j in range(tests_in_epoch):
            predict = find_segments(fit_pics[j], params)
            error += segments_error(predict, fit_answers[j], max_penalty)

        if i < 20 or i % 50 == 0:
            print(i, "-th epoch complete")

        if error < best_error:
            best_error = error
            best_params = params
            print("New best result:", best_error / tests_in_epoch, best_params)
    return best_params, best_error


if __name__ == "__main__":
    print(find_segments_fit(10**4, 6, 100))
