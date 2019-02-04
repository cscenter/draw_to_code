import cv2
import numpy as np
from PIL import Image

from geometry import Point, Segment, Circle, Line
import pic_generator
from latex_pic_generator import convert_to_latex

STD_PARAMS_SEGMENT_OPENCV_PROB = (1, np.pi/180, 20, 20, 30)


def find_segments_opencv_probalistic(image, params=STD_PARAMS_SEGMENT_OPENCV_PROB):
    ro_step, theta_step, threshold, min_len, max_len = params
    segments = cv2.HoughLinesP(image, ro_step, theta_step, threshold, min_len, max_len)
    result = []
    for segl in segments:
        x1, y1, x2, y2 = segl[0]
        result.append(Segment(Point(x1, y1), Point(x2, y2)))
    return result


def find_lines_opencv(image, params):
    ro_step, theta_step, threshold = params
    lines = cv2.HoughLines(image, ro_step, theta_step, threshold)
    result = []
    for line in lines:
        ro, theta = line[0]
        result.append(Line.line_by_ro_theta(ro, theta))
    return result


def find_and_draw_segments(image, params, pic_size,
                           filename="hough_result",
                           find=find_segments_opencv_probalistic):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)[1]
    segments = find(image, params)
    res_pic = pic_generator.generate_pil_image(segments, pic_size)
    pic_generator.save_pil_image(res_pic, "pics/{}".format(filename))
    print(convert_to_latex(segments))


if __name__ == "__main__":
    pic_size = 400
    in_image = pic_generator.generate_random_pic(pic_size, 0, 5, 0)[0]
    pic_generator.save_pil_image(in_image, "pics/hough_test_input")
    img = cv2.imread("pics/hough_test_input.png")
    find_and_draw_segments(img, STD_PARAMS_SEGMENT_OPENCV_PROB, pic_size)
