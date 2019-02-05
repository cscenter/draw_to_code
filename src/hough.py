import cv2
import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.filters import gaussian
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt

from geometry import Point, Segment, Circle, Line
import pic_generator
from latex_pic_generator import convert_to_latex

STD_PARAMS_SEGMENT_OPENCV_PROB = (1, np.pi/180, 20, 20, 30)
STD_PARAMS_LINES_SKIMAGE = (30, 20, 30, 30, 0)
STD_PARAMS_SEGMENTS_SKIMAGE = (*STD_PARAMS_LINES_SKIMAGE, 30, 1, 400)


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
params: min_dist, min_angel, threshold, num_peaks, sigma
    min_dist: minimum distance between lines to pick them both
    min_angle: similarly for angle
    threshold: minimum value for line in accum array to pick it
    num_peaks: maximum amount of picked line
    sigma: standart deviation when we smooth hough space
    
RETURN: two arrays, result and accum
result: list of Line objects - founded lines 
accum: "brightnesses" of lines
"""
def find_lines(image, params = STD_PARAMS_LINES_SKIMAGE):
    min_dist, min_angle, threshold, num_peaks, sigma = params
    hspace, angels, distances = hough_line(image)
    noized_hspace = hspace #  gaussian(hspace, sigma=sigma)
    accum, thetas, ros = hough_line_peaks(noized_hspace.copy(), angels, distances,
                                          min_dist, min_angle, threshold, num_peaks)
    result = [Line.line_by_ro_theta(ros[i], thetas[i]) for i in range(len(ros))]
    return result, accum, hspace, noized_hspace


def find_segments(image, params=STD_PARAMS_SEGMENTS_SKIMAGE):
    min_dist, min_angel, thr_hough, num_peaks, sigma, min_segment_len, window_size, thr_segs = params
    lines = find_lines(image, (min_dist, min_angel, thr_hough, num_peaks, sigma))[0]
    ans = []

    for line in lines:
        way = line.cross_with_rect(Point(0, 0), Point(image.shape[1], image.shape[0]))
        if way is None:
            print("Warning: line doesn't intersect image (hough.py, def find_segments)")
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

