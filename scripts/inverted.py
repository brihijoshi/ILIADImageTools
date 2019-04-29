from skimage import data, io, segmentation, color
from skimage.future import graph
import numpy as np
import matplotlib.image as mpimg
from skimage.io import imread
from skimage.transform import warp
from skimage.transform import swirl
from skimage import util
from skimage.transform import PiecewiseAffineTransform, warp


image = imread('coffee.png')

hsv = color.rgb2hsv(image)
hsv = color.hsv2rgb(hsv)

print(type(hsv[0,0,0]))

io.imshow(out)
io.show()
