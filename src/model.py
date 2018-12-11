import numpy as np

import models.circle as circle_model
import models.segment as segment_model
import pic_generator
from geometry import Circle, Segment, Point


class Model:
    def __init__(self, image_size):
        self.image_size = image_size
        self._load_weights()

    def _load_weights(self):
        image_size = self.image_size

        self.find_circle_model = circle_model.find_circle_model(image_size)
        self.find_circle_model.load_weights("find_circle_model.h5")

        self.get_circle_model = circle_model.get_circle_model(image_size)
        self.get_circle_model.load_weights("get_circle_model.h5")

        self.find_segment_model = segment_model.find_segment_model(image_size)
        self.find_segment_model.load_weights("find_segment_model.h5")

        self.get_segment_model = segment_model.get_segment_model(image_size)
        self.get_segment_model.load_weights("get_segment_model.h5")

    def _im_to_x(self, im):
        return np.array([np.array(im)]).reshape(1, self.image_size, self.image_size, 1)

    def find_circle(self, im):
        x = self._im_to_x(im)
        res = self.find_circle_model.predict_classes(x)
        return res[0] == 1

    def get_circle(self, im):
        x = self._im_to_x(im)
        res = self.get_circle_model.predict(x)
        return Circle.construct_from_y(res[0], self.image_size)

    def find_segment(self, im):
        x = self._im_to_x(im)
        res = self.find_segment_model.predict_classes(x)
        return res[0] == 1

    def get_segment(self, im):
        x = self._im_to_x(im)
        res = self.get_segment_model.predict(x)
        return Segment.construct_from_y(res[0], self.image_size)

    def _get_new_image(self, im, figure):
        if isinstance(figure, Circle):
            radius = figure.radius
            for delta in range(-5, 6):
                figure.radius = radius + delta
                figure_image = pic_generator.generate_pil_image([figure], self.image_size)
                im = pic_generator.subtract_image(im, figure_image)
        else:
            figure_image = pic_generator.generate_pil_image([figure], self.image_size)
            im = pic_generator.subtract_image(im, figure_image)
        return im

    def solve(self, image):
        MAX_ITERATIONS = 5
        im = image.copy()
        images = [im]

        circles = []
        iterations = 0
        while self.find_circle(im):
            if iterations == MAX_ITERATIONS:
                break
            iterations += 1
            print(1)
            circle = self.get_circle(im)
            circles.append(circle)
            images.append(pic_generator.generate_pil_image([circle], self.image_size))
            im = self._get_new_image(im, circle)
            images.append(im)

        segments = []
        iterations = 0
        while self.find_segment(im):
            if iterations == MAX_ITERATIONS:
                break
            iterations += 1
            print(2)
            segment = self.get_segment(im)
            segment.width = 8
            segments.append(segment)
            images.append(pic_generator.generate_pil_image([segment], self.image_size))
            im = self._get_new_image(im, segment)
            images.append(im)

        return circles, segments, images
