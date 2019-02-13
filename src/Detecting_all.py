import os

import numpy as np
import pic_generator
from PIL import Image, ImageOps
from PyPDF2 import PdfFileWriter, PdfFileReader
from detect_circles import find_circles
from detect_segm import find_segments, draw_segments
from helper import to_pdf
from hough import find_segments as find_segments_1
from latex_pic_generator import convert_to_latex
from matplotlib import pyplot as plt
from pic_generator import subtract_image
from Project_to_circles import last_changes, unite_similar, normalize

from skimage import data, io

def main(file_path='test_images/simple.png', count_circles=-1):
    #file_path = 'test_images/simple.png'
    key = 2
    if key == 1:
        #image = io.imread(file_path)
        image = pic_generator.load_image(file_path)
        image = np.array(image)
        # If use_sobel == 1, we add lines from Hough transform after Sobel filter. But it works slower
        final_list_of_segments = find_segments(image, use_sobel=0)
    else:
        image = pic_generator.load_image(file_path)
        image = np.array(ImageOps.invert(image))
        final_list_of_segments = find_segments_1(image)
        for Seg in final_list_of_segments:
            tmp_px = Seg.point_1.x
            Seg.point_1.x = Seg.point_1.y
            Seg.point_1.y = tmp_px
            tmp_px = Seg.point_2.x
            Seg.point_2.x = Seg.point_2.y
            Seg.point_2.y = tmp_px
        image = 255 - image
    image_detected_segm = draw_segments(image, final_list_of_segments)
    #fig, axis = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    #axis.imshow(image_detected_segm)
    #plt.show()
    image_pil = Image.fromarray(image)
    subtract = subtract_image(image_pil, image_detected_segm)
    #subtract.show()
    image = np.array(subtract)
    final_list_of_circles = find_circles(image, count_circles)
    final_list_of_segments = last_changes(final_list_of_segments, final_list_of_circles)
    final_list_of_segments = unite_similar(final_list_of_segments)
    final_list_of_segments, final_list_of_circles = normalize(max(image.shape[0], image.shape[1]), image.shape[0], final_list_of_segments, final_list_of_circles)
    #print(.project_point_seg())

    template_tex = convert_to_latex(final_list_of_segments + final_list_of_circles)
    to_pdf('output', template_tex, '')
    '''output = PdfFileWriter()
    with open("rotated.pdf", "rb") as f:
        input_pdf = PdfFileReader(f)
        output_file = open("output.pdf", "wb")
        output.addPage(input_pdf.getPage(0).rotateClockwise(90))
        output.write(output_file)
        output_file.close()
    os.remove('rotated.pdf')
    #os.remove('rotated.log')
    #os.remove('rotated.tex')
    #os.remove('rotated.aux')'''
    output_tex = open("output.tex", "w")
    output_tex.write(template_tex)
    output_tex.close()
    return template_tex


if __name__ == '__main__':
    main()
