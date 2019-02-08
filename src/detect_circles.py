from copy import copy
from skimage import data, io
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.morphology import binary_erosion, skeletonize, binary_closing, binary_opening, binary_dilation, remove_small_holes
from skimage.morphology import disk

def cust(u, v):
    ans = np.zeros((u.shape[0], u.shape[1]))
    for i in range(u.shape[0]):
        for j in range(u.shape[1]):
            if u[i][j] == 255 and v[i][j] == 0:
                ans[i][j] = 255
    return ans

image = io.imread('black_circles.bmp')
image = 255 - image
#selem = disk(2)
#thickimage = binary_dilation(image, selem)
#thickimage = np.uint8(thickimage)*255
io.imshow(image)
plt.show()
prev_proc = sum(sum(image))/(image.shape[0]*image.shape[1])/255
# Load picture and detect edges
#image = img_as_ubyte(data.coins()[160:230, 70:270])
final_list_of_circles = []
for indd in range(18):
    edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)
    minim_radii = int(min(image.shape[0], image.shape[1])/20)
    maxim_radii = int(min(image.shape[0], image.shape[1])/2)
    stepp = 1
    if (maxim_radii - minim_radii) > 200:
        stepp = 2
    if (maxim_radii - minim_radii) > 400:
        stepp = 4
    hough_radii = np.arange(minim_radii, maxim_radii, stepp)
    hough_res = hough_circle(edges, hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks = 1)
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    image1 = np.zeros((image.shape[0], image.shape[1]))
    #image1 = copy(image)#color.gray2rgb(image)
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius)
        for ccy, ccx in zip(circy, circx):
            if 0 < ccy < image.shape[0] and 0 < ccx < image.shape[1]:
                image1[ccy][ccx] = 255#(255, 20, 20)#circy, circx] = (220, 20, 20)
    selem = disk(5)
    thickimage1 = binary_dilation(image1, selem)
    thickimage1 = np.uint8(thickimage1)*255    
    image = cust(image, thickimage1)
    white_proc= sum(sum(image))/(image.shape[0]*image.shape[1])/255
    print(white_proc)
    if abs(white_proc - prev_proc) < 0.0009:
        #print(white_proc - prev_proc)
        break
    for center_y, center_x, radius in zip(cy, cx, radii):
        final_list_of_circles.append((center_y, center_x, radius))
    prev_proc = white_proc
    if white_proc < 0.005:
        break
    ax.imshow(image, cmap=plt.cm.gray)
    plt.show()