from geometry import Circle, Point, Segment, Line
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from math import *
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage import io, data
from skimage.feature import corner_harris, corner_subpix, corner_peaks
from skimage.draw import ellipse, line, line_aa

from copy import copy

from sklearn.cluster import KMeans
import numpy as np


def is_seg_on_line(Lin, Seg):
    d1 = Lin.dist_to_point(Seg.point_1)
    d2 = Lin.dist_to_point(Seg.point_2)
    #EPS = 15
    #if d1 < EPS and d2 < EPS:
    #    return max(d1, d2)
    return max(d1, d2)


def boundary_by_2_means(list_of_proc):
    is_good = True
    list_of_proc = np.array(list_of_proc)
    x = np.array(copy(list_of_proc[:, 0]))
    km = KMeans(n_clusters=2)
    km.fit(x.reshape(len(x), 1))
    km1 = copy(km.labels_)
    km.labels_.sort()
    if not (np.array_equal(km.labels_, km1) or np.array_equal(km.labels_, km1[::-1])):
        # print("Error in clustering")
        is_good = False
    ind_between = min(np.where(km1 == 1)[0])
    bound = 0
    if ind_between > 0:
        bound = 0.5 * (x[ind_between] + x[ind_between - 1])
    # if bound > 0.4:
    ##print("Probably there is an error, bound =", bound)
    # bound = 0.1
    # is_good = False
    return is_good, bound


def find_by_diff(list_of_proc):
    list_of_proc = np.array(list_of_proc)
    x = copy(list_of_proc[:, 0])
    best_i = 1
    best_metr = 10000
    for i in range(1, len(x)):
        metr = x[i - 1] - x[i] + x[i - 1]
        if metr < best_metr:
            best_i = i
            best_metr = metr
    bound = 0
    if best_i > 0:
        bound = 0.5 * (x[best_i] + x[best_i - 1])
    return bound


def count_proc(P, Q, image):
    our_line = Line.line_by_two_points(P, Q)
    thresh = 2
    cou_b = 0
    cou_w = 0
    # print(max(min(py, qy) - thresh, 0), min(max(px, qx) + 1 + thresh, image.shape[1]))
    for i in range(max(min(P.x, Q.x) - thresh, 0), min(max(P.x, Q.x) + 1 + thresh, image.shape[0])):
        for j in range(max(min(P.y, Q.y) - thresh, 0), min(max(P.y, Q.y) + 1 + thresh, image.shape[1])):
            cur_P = Point(i, j)
            dis = our_line.dist_to_point(cur_P)
            if dis < thresh:
                if image[i][j] < 70:
                    cou_b += 1
                else:
                    cou_w += 1
    proc = cou_b / (cou_b + cou_w)
    return proc


image = io.imread('test_images/big5.bmp')
#io.imshow(image)
coords = corner_peaks(corner_harris(image), min_distance=15)
coords_subpix = corner_subpix(image, coords, window_size=13)
# plt.show()
fig, ax = plt.subplots()
ax.imshow(image, interpolation='nearest', cmap=plt.cm.gray)
ax.plot(coords[:, 1], coords[:, 0], '.b', markersize=10)
ax.plot(coords_subpix[:, 1], coords_subpix[:, 0], '+r', markersize=15)
ax.axis((0, image.shape[1], image.shape[0], 0))

num_corners = len(coords)
list_of_proc = []
for i1 in range(num_corners):
    for i2 in range(i1 + 1, num_corners):
        px = coords[:, 0][i1]  # x это по вертикали как в image
        py = coords[:, 1][i1]
        qx = coords[:, 0][i2]
        qy = coords[:, 1][i2]
        P = Point(px, py)
        Q = Point(qx, qy)
        proc = count_proc(P, Q, image)
        list_of_proc.append((proc, i1, i2))
        # if proc > 0.1:
        # print("seg", i1, i2, px, py, qx, qy)
        ##else:
        ##print(i1, i2, cou_b, cou_w, proc, px, py, qx, qy)
list_of_proc.sort()
plt.show()
# Three variants of threshold
is_good, bound = boundary_by_2_means(list_of_proc)
bound1 = find_by_diff(list_of_proc)
bound2 = 0.1
bound_fin = 0
if is_good:
    bound_fin = 0.45 * bound1 + 0.35 * bound2 + 0.2 * bound
else:
    bound_fin = 0.6 * bound1 + 0.4 * bound2
# Draw what we have found
segm_init = []
#img = copy(image)
#img = np.zeros([image.shape[0], image.shape[1]])
for (proc, i1, i2) in list_of_proc:
    i1 = int(i1)
    i2 = int(i2)
    if proc > bound_fin:
        print("seg", i1, i2, coords[:, 0][i1], coords[:, 1][i1], coords[:, 0][i2], coords[:, 1][i2])
        #rr, cc = line(coords[:, 0][i1], coords[:, 1][i1], coords[:, 0][i2], coords[:, 1][i2])
        #img[rr, cc] = 100
        point1 = Point(coords[:, 0][i1], coords[:, 1][i1])
        point2 = Point(coords[:, 0][i2], coords[:, 1][i2])
        segm_init.append(Segment(point1, point2))
# Hoff
list_of_lines = []  # from hough in form of classes
h, theta, d = hough_line(255 - image)
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    list_of_lines.append(Line.line_by_ro_theta(dist, angle))
seg_for_each_line = [set([]) for i in range(len(list_of_lines))]

segm_final = []
for Seg in segm_init:
    num_line = -1
    min_dist = 100000
    for (i, Lin) in enumerate(list_of_lines):
        new_dist = is_seg_on_line(Lin, Seg)
        if new_dist < min_dist:
            min_dist = new_dist
            num_line = i
    if min_dist < 8:
        seg_for_each_line[num_line].add((Seg.point_1.x, Seg.point_1.y))
        seg_for_each_line[num_line].add((Seg.point_2.x, Seg.point_2.y))
    else:
        procc = count_proc(Seg.point_1, Seg.point_2, image)
        if procc > 0.3:
            segm_final.append(Seg)
            #print("spec", procc, (Seg.point_1.x, Seg.point_1.y, Seg.point_2.x, Seg.point_2.y))
for i in range(len(list_of_lines)):
    curlist = list(seg_for_each_line[i])
    if len(curlist) == 0:
        continue
    delx = max(curlist, key = lambda tup: tup[0])[0] - min(curlist, key = lambda tup: tup[0])[0]
    dely = max(curlist, key = lambda tup: tup[1])[1] - min(curlist, key = lambda tup: tup[1])[1]
    if delx > dely:
        curlist.sort()
    else:
        curlist = sorted(curlist, key = lambda tup: tup[1])
    have_seg = [0 for qq in range(len(curlist) - 1)]
    for j in range(len(curlist) - 1):
        P = Point(curlist[j][0], curlist[j][1])
        Q = Point(curlist[j + 1][0], curlist[j + 1][1])
        proc = count_proc(P, Q, image)
        if proc > bound_fin:
            have_seg[j] = 1
    j = 0
    while j < len(have_seg):
        while j < len(have_seg) and have_seg[j] == 0:
            j += 1
        if j < len(have_seg):
            start = Point(curlist[j][0], curlist[j][1])
            while j < len(have_seg) and have_seg[j] == 1:
                j += 1
            if j != len(have_seg):
                finish = Point(curlist[j][0], curlist[j][1])
            else:
                finish = Point(curlist[j][0], curlist[j][1])
            segm_final.append(Segment(start, finish))
            print((start.x, start.y, finish.x, finish.y))
#img = np.zeros([image.shape[0], image.shape[1]])
img = Image.new("RGBA", (image.shape[1], image.shape[0]), (0,0,0,1))
draw = ImageDraw.Draw(img)
for Seg in segm_final:
    #Seg.to_pil(draw)
    P1 = Seg.point_1
    P2 = Seg.point_2
    draw.line([(int(P1.y), int(P1.x)), (int(P2.y), int(P2.x))], fill = "red", width=3)
    #rr, cc, val = line_aa(int(P1.x), int(P1.y), int(P2.x), int(P2.y))
    #img[rr, cc] = 255 * val
del draw
img.save("pil_vis.png", "PNG")
#io.imshow(img)
#plt.show()