from skimage import color, segmentation
import skimage.io as io
import os
import matplotlib
import matplotlib.pyplot as plt

# os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
pic = io.imread('test_0.png')
io.imshow(pic)
plt.show()
print('1')
