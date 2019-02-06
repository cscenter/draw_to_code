import cv2
import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.filters import gaussian
from random import choice, randint
from PIL import ImageOps

from geometry import Point, Segment, Circle, Line
import pic_generator

STD_PARAMS_SEGMENT_OPENCV_PROB = (1, np.pi/180, 20, 20, 30)

STD_PARAMS_LINES_SKIMAGE = (2, 7, 40, 20)
STD_PARAMS_SEGMENTS_SKIMAGE = (*STD_PARAMS_LINES_SKIMAGE, 30, 2, 300)

# deprecated, worse than new methods
def find_segments_opencv_probalistic(image, params=STD_PARAMS_SEGMENT_OPENCV_PROB):
    ro_step, theta_step, threshold, min_len, max_len = params
    segments = cv2.HoughLinesP(image, ro_step, theta_step, threshold, min_len, max_len)
    result = []
    for segl in segments:
        x1, y1, x2, y2 = segl[0]
        result.append(Segment(Point(x1, y1), Point(x2, y2)))
    return result


"""
ARGUMENTS:
image: numpy array(N, M), every element is integer in [0, 255].
params: min_dist, min_angel, threshold, num_peaks
    min_dist: minimum distance between lines to pick them both
    min_angle: similarly for angle
    threshold: minimum value for line in accum array to pick it
    num_peaks: maximum amount of picked line
    
RETURN: three arrays - result, accum and hspace
result: list of Line objects - founded lines 
accum: "brightnesses" of lines
hspace: hough space
"""
def find_lines(image, params = STD_PARAMS_LINES_SKIMAGE):
    min_dist, min_angle, threshold, num_peaks = params
    hspace, angels, distances = hough_line(image)
    accum, thetas, ros = hough_line_peaks(hspace, angels, distances,
                                          min_dist, min_angle, threshold, num_peaks)
    result = [Line.line_by_ro_theta(ros[i], thetas[i]) for i in range(len(ros))]
    return result, accum, hspace


"""
ARGUMENTS:
image: numpy array(N, M), every element is integer in [0, 255].
params: min_dist, min_angel, thr_hough, num_peaks, min_segment_len, window_size, thr_segs
    first 4 arguments: like in find_hough function
    min_segment_len: minimum length of detectable segment
    window_size: how many pixels around line we look at
    thr_segs - minimum sum of pixels in window to mark current pixel as black

RETURN: list of Segment objects - segments on a picture
"""
def find_segments(image, params=STD_PARAMS_SEGMENTS_SKIMAGE):
    min_dist, min_angel, thr_hough, num_peaks, min_segment_len, window_size, thr_segs = params
    lines = find_lines(image, (min_dist, min_angel, thr_hough, num_peaks))[0]
    ans = []

    for line in lines:
        way = line.cross_with_rect(Point(0, 0), Point(image.shape[1], image.shape[0]))
        if way is None:
            # print("Warning: line doesn't intersect image (hough.py, def find_segments)")
            continue

        dir = way.point_2 - way.point_1
        dir = dir.norm()
        start = way.point_1

        cur = start
        strick = 0
        while Point.distance_between(start, cur) < Point.distance_between(start, way.point_2):
            cur_pixel = (int(np.round(cur.y)), int(np.round(cur.x)))
            pixels_to_check = []
            for i in range(-window_size, window_size + 1):
                for j in range(-window_size, window_size + 1):
                    pixels_to_check.append((cur_pixel[0] + i, cur_pixel[1] + j))

            brightnes = 0
            for pix in pixels_to_check:
                try:
                    brightnes += image[pix[0]][pix[1]]
                except IndexError:
                    pass

            if brightnes >= thr_segs:
                if strick == 0:
                    seg_start = cur
                strick += 1
            else:
                if strick >= min_segment_len:
                    ans.append(Segment(seg_start, cur))
                strick = 0
            cur = cur + dir
    return ans


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


def find_segments_fit(im_size, epochs, tests_in_epoch, max_penalty):
    params_variants = [
        [0, 1, 2, 3, 5, 7, 10, 12, 15, 20, 30], # min dist
        [0, 1, 2, 3, 5, 7, 10, 12, 15, 20, 25], # min angle
        [0, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 70, 100], # threshold hough
        [5, 10, 20, 30, 40], # num peaks
        [3, 5, 7, 10, 15, 20, 30, 40, 50, 70, 100], # min seg len
        [0, 1, 2, 3], # window size
        [200, 300, 400, 500, 800, 1000, 1500] # threshold seg
    ]

    best_error = np.inf
    best_params = None
    for i in range(epochs):
        params = [choice(vars) for vars in params_variants]
        error = 0
        for j in range(tests_in_epoch):
            pic, ans = pic_generator.generate_random_pic(im_size,
                                                         segments_amount=randint(0, 5),
                                                         circles_amount=randint(0, 3))
            ans = [a for a in ans if isinstance(a, Segment)]
            nimage = np.array(ImageOps.invert(pic))
            predict = find_segments(nimage, params)
            error += segments_error(predict, ans, max_penalty)

        if error < best_error:
            best_error = error
            best_params = params
            print("New best result:", best_error, best_params)
        print(i, "-th epoch complete")
    return best_params, best_error


if __name__ == "__main__":
    print(find_segments_fit(200, 10**4, 100, 100))