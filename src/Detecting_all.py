from latex_pic_generator import convert_to_latex
from helper import to_pdf
from detect_segm import find_segments, draw_segments
from detect_circles import find_circles
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from skimage import io
import numpy as np
from pic_generator import subtract_image
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

image = io.imread('test_images/big2.bmp')
final_list_of_segments = find_segments(image)
img = draw_segments(image, final_list_of_segments)
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
ax.imshow(img)
plt.show()
imagepil = Image.fromarray(image)
sub = subtract_image(imagepil, img)
sub.save("substr.bmp", "BMP")
sub.show()
image = np.array(sub)
final_list_of_circles = find_circles(image)
Templ = convert_to_latex(final_list_of_segments + final_list_of_circles)
to_pdf('name1', Templ, '')
output = PdfFileWriter()
with open("name1.pdf", "rb") as f:
    input_pdf = PdfFileReader(f)
    output_file = open("output.pdf", "wb")
    output.addPage(input_pdf.getPage(0).rotateClockwise(90))
    output.write(output_file)
    output_file.close()
os.remove('name1.pdf')
os.remove('name1.log')
os.remove('name1.tex')
os.remove('name1.aux')
outputtex = open("output.tex", "w")
outputtex.write(Templ)
outputtex.close()