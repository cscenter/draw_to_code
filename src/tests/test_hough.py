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
import fit_hough
from hough import find_lines, find_segments

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


    out_im = Image.open("../../pics/hough_test_input.png")
    draw = ImageDraw.Draw(out_im)
    for i, l in enumerate(lines):
        print("a = {}, b = {}, c = {}, accum = {}".format(l.a, l.b, l.c, accum[i]))
        l.to_pil(draw, max(nim.shape[0], nim.shape[1]), color='red')
    pic_generator.save_pil_image(out_im, "../../pics/hough_test_output")


def test_segments(filename, out_name = "hough_test_output"):
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
    pic_generator.save_pil_image(out_im, "../../pics/{}".format(out_name))


def draw_answer(test_num):
    segs = fit_hough.load_segments_list("../../pics/ans{}.txt".format(test_num))
    out_im = Image.new('L', (200, 200), 255)
    draw = ImageDraw.Draw(out_im)
    for s in segs:
        s.to_pil(draw)
    pic_generator.save_pil_image(out_im, "../../pics/kek_test_output")


if __name__ == "__main__":
    test_hough("bettertrain5input.png")
    #for i in range(10):
        #test_segments("bettertrain{}input.png".format(i), "bettertrain{}result".format(i))
