from skimage import data, io, segmentation, color
from skimage.future import graph
import numpy as np
import matplotlib.image as mpimg
from skimage.io import imread
from skimage.transform import warp
from skimage.transform import swirl
from skimage import util


img = imread('coffee.png')

img_gray = color.rgb2gray(img)

print(img_gray)

rgb = color.gray2rgb(img_gray)
hsv = color.rgb2hsv(rgb)
print(hsv)
hsv[:, :, 1] = 1
print(hsv)
print(color.hsv2rgb(hsv))

io.imshow(color.hsv2rgb(hsv))
io.show()