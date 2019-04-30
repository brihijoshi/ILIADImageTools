from skimage import data, io, segmentation, color
from skimage.future import graph
import numpy as np
import matplotlib.image as mpimg
from skimage.io import imread
from skimage.transform import warp
from skimage.transform import swirl
from skimage import util
from skimage.transform import PiecewiseAffineTransform, warp
from skimage.measure import block_reduce



image = np.arange(9*3*3).reshape(9, 3, 3)

print(len(image))
print(len(image[0]))
print(len(image[0][0]))
t1= block_reduce(image, block_size=(1, 1, 2), func=np.mean)
print('----')
print(t1)
print(t1.shape)

# image = color.gray2rgb(color.rgb2gray(image))

# print(image)
# io.imshow(image)
# io.show()

# lst1 = [1, 2, 3]
# lst2 = lst1
# del lst1[:]
# print(lst1)
# print(lst2)

# print(image)


# for i in range(len(image[0])):
#     for j in range(len(image)):
#         print(image[j][i])


