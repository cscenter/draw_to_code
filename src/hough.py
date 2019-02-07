import cv2
import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.filters import gaussian
from random import choice, randint
from PIL import ImageOps

from geometry import Point, Segment, Circle, Line
import pic_generator

STD_PARAMS_LINES_SKIMAGE = (30, 10, 15, 10)
STD_PARAMS_SEGMENTS_SKIMAGE = (*STD_PARAMS_LINES_SKIMAGE, 40, 1, 500)

"""
ARGUMENTS:
image: numpy array(N, M), every element is integer in [0, 255].
params: min_dist, min_angel, threshold, num_peaks
    min_dist: minimum distance between lines to pick them both
    min_angle: similarly for angle
    threshold: minimum value for line in accum array to pick it
    num_peaks: maximum amount of picked line
    
RETURN: three arrays - result, accum and hspace
    lines: list of Line objects - founded lines 
    accum: "brightnesses" of lines
    hspace: hough space
"""
def find_lines(image, min_dist=30, min_angle=10, threshold=15, num_peaks=10, angles_count=720):
    hspace, angels, distances = hough_line(image, np.linspace(-np.pi/2, np.pi/2, angles_count))
    accum, thetas, ros = hough_line_peaks(hspace, angels, distances,
                                          min_dist, min_angle, threshold, num_peaks)
    lines = [Line.line_by_ro_theta(ros[i], thetas[i]) for i in range(len(ros))]
    return lines, accum, hspace


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
def find_segments(image, min_dist=30, min_angel=7, thr_hough=50, num_peaks=30, angles_count=270,
                  min_segment_len=40, window_size=1, thr_segs=750):
    lines = find_lines(image, min_dist, min_angel, thr_hough, num_peaks, angles_count)[0]
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
