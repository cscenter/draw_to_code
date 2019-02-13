from geometry_generator import generate_segment
from PIL import Image, ImageChops, ImageDraw
import numpy as np

seg = generate_segment(100)
im = Image.new('L', (100, 100), 255)
draw = ImageDraw.Draw(im)
seg.to_pil(draw)
im.save("pics/fourwidthsegment.png")