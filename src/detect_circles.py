import matplotlib.pyplot as plt
import numpy as np
from geometry import Circle, Point
from skimage.draw import circle_perimeter
from skimage.feature import canny
from skimage.morphology import binary_dilation
from skimage.morphology import disk
from skimage.transform import hough_circle, hough_circle_peaks


def subtract_skimage(u, v):
    ans = np.zeros((u.shape[0], u.shape[1]))
    for i in range(u.shape[0]):
        for j in range(u.shape[1]):
            if u[i][j] == 255 and v[i][j] == 0:
                ans[i][j] = 255
    return ans


def find_circles(image, count_):
    image = 255 - image
    image[np.where(image > 170)] = 255.
    image = np.array(image, dtype='float64')
    prev_proc = sum(sum(image)) / (image.shape[0] * image.shape[1]) / 255.
    # 0.17, 0.031 are constants based on example 'many_circles.bmp'
    if count_ == -1:
        bord1 = 0.17 * prev_proc
        bord2 = 0.031 * prev_proc
    else:
        bord1 = -10000
        bord2 = -10000
    final_list_of_circles = []
    max_amount_of_circles = 18
    if count_ != -1:
        max_amount_of_circles = int(count_)
    for indd in range(max_amount_of_circles):
        edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)
        minim_radii = int(min(image.shape[0], image.shape[1])/20)
        maxim_radii = int(min(image.shape[0], image.shape[1])/2)
        # Adapt step in Hough transform if picture is too big
        stepp = 1
        if (maxim_radii - minim_radii) > 200:
            stepp = 2
        if (maxim_radii - minim_radii) > 400:
            stepp = 4
        hough_radii = np.arange(minim_radii, maxim_radii, stepp)
        hough_res = hough_circle(edges, hough_radii)
        accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
        image1 = np.zeros((image.shape[0], image.shape[1]))
        for center_y, center_x, radius in zip(cy, cx, radii):
            circy, circx = circle_perimeter(center_y, center_x, radius)
            for ccy, ccx in zip(circy, circx):
                if 0 < ccy < image.shape[0] and 0 < ccx < image.shape[1]:
                    image1[ccy][ccx] = 255
        # Thick segments before subtracting
        selem = disk(5)
        thickimage1 = binary_dilation(image1, selem)
        thickimage1 = np.uint8(thickimage1)*255
        image = subtract_skimage(image, thickimage1)
        white_proc = sum(sum(image))/(image.shape[0]*image.shape[1])/255
        # if prev iteration is very similar to new iteration, stop
        if abs(white_proc - prev_proc) < 0.3 * bord2 + 0.7 * 0.0009:
            break
        for center_y, center_x, radius in zip(cy, cx, radii):
            final_list_of_circles.append(Circle(Point(center_y, center_x), radius))
        prev_proc = white_proc
        # if procent of white pixels is too small, stop
        if white_proc < 0.3 * bord1 + 0.7 * 0.005:
            break
    #ax.imshow(image, cmap=plt.cm.gray)
    #plt.show()
    return final_list_of_circles
