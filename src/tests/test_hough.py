import cv2
import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.filters import gaussian
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt

from geometry import Point, Segment, Circle, Line
import pic_generator
from latex_pic_generator import convert_to_latex

import hough
from hough import find_lines, find_segments, find_segments_opencv_probalistic


def find_and_draw_segments(image, params, pic_size,
                           filename="hough_result"):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)[1]
    segments = find_segments_opencv_probalistic(image, params)
    res_pic = pic_generator.generate_pil_image(segments, pic_size)
    pic_generator.save_pil_image(res_pic, "pics/{}".format(filename))
    print(convert_to_latex(segments))


def test_prob_hough():
    pic_size = 400
    in_image = pic_generator.generate_random_pic(pic_size, 0, 5, 0)[0]
    pic_generator.save_pil_image(in_image, "pics/hough_test_input")
    img = cv2.imread("pics/hough_test_input.png")
    find_and_draw_segments(img, hough.STD_PARAMS_SEGMENT_OPENCV_PROB, pic_size)


def save_array_as_image(array: np.array, path):
    mean = array.mean()
    print(mean, np.median(array))
    a = np.log(1 + array/mean)
    pic_generator.save_pil_image(Image.fromarray(a, 'I'),
                                 path)


def test_hough(filename):
    in_image = pic_generator.load_image("../../pics/{}".format(filename))
    pic_generator.save_pil_image(in_image, "../../pics/hough_test_input")
    nim = np.array(ImageOps.invert(in_image))
    print("Picture size:", nim.shape)

    lines, accum, hough = find_lines(nim)


    out_im = Image.new('L', (nim.shape[1], nim.shape[0]), 255)
    draw = ImageDraw.Draw(out_im)
    for i, l in enumerate(lines):
        print("a = {}, b = {}, c = {}, accum = {}".format(l.a, l.b, l.c, accum[i]))
        l.to_pil(draw, max(nim.shape[0], nim.shape[1]))
    pic_generator.save_pil_image(out_im, "../../pics/hough_test_output")


def test_gaussian(filename):
    in_image = pic_generator.load_image("../../pics/{}".format(filename))
    pic_generator.save_pil_image(in_image, "../../pics/gaussian_test_input")
    nim = np.array(in_image)
    nout = gaussian(nim, sigma=0)
    pic_generator.save_pil_image(Image.fromarray(nim, 'I'),
                                 "../../pics/gaussian_test_output")


def test_segments(filename):
    in_image = pic_generator.load_image("../../pics/{}".format(filename))
    pic_generator.save_pil_image(in_image, "../../pics/hough_test_input")
    nim = np.array(ImageOps.invert(in_image))
    print("Picture size:", nim.shape)

    segs = find_segments(nim)

    out_im = Image.new('L', (nim.shape[1], nim.shape[0]), 255)
    draw = ImageDraw.Draw(out_im)
    for s in segs:
        print("x1 = {}, y1 = {}, x2 = {}, y2 = {}".format(s.point_1.x,
                                                          s.point_1.y,
                                                          s.point_2.x,
                                                          s.point_2.y))
        s.to_pil(draw)
    pic_generator.save_pil_image(out_im, "../../pics/hough_test_output")


if __name__ == "__main__":
    test_segments("output.bmp")
