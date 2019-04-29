from skimage import io, segmentation
from skimage.color import convert_colorspace, rgba2rgb, hsv2rgb, rgb2gray, label2rgb
from skimage.future import graph
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def _weight_mean_color(graph, src, dst, n):
	"""Callback to handle merging nodes by recomputing mean color.

	The method expects that the mean color of `dst` is already computed.

	Parameters
	----------
	graph : RAG
		The graph under consideration.
	src, dst : int
		The vertices in `graph` to be merged.
	n : int
		A neighbor of `src` or `dst` or both.

	Returns
	-------
	data : dict
		A dictionary with the `"weight"` attribute set as the absolute
		difference of the mean color between node `dst` and `n`.
	"""

	diff = graph.node[dst]['mean color'] - graph.node[n]['mean color']
	diff = np.linalg.norm(diff)
	return {'weight': diff}


def merge_mean_color(graph, src, dst):
	"""Callback called before merging two nodes of a mean color distance graph.

	This method computes the mean color of `dst`.

	Parameters
	----------
	graph : RAG
		The graph under consideration.
	src, dst : int
		The vertices in `graph` to be merged.
	"""
	graph.node[dst]['total color'] += graph.node[src]['total color']
	graph.node[dst]['pixel count'] += graph.node[src]['pixel count']
	graph.node[dst]['mean color'] = (graph.node[dst]['total color'] /
									 graph.node[dst]['pixel count'])

image_file_inverted = mpimg.imread('coffee.png')

# image_file_inverted = np.float64(image_file)

labels = segmentation.slic(image_file_inverted, compactness=30, n_segments=400)
g = graph.rag_mean_color(image_file_inverted, labels)

labels2 = graph.merge_hierarchical(labels, g, thresh=35, rag_copy=False,
								   in_place_merge=True,
								   merge_func=merge_mean_color,
								   weight_func=_weight_mean_color)

out = label2rgb(labels2, image_file_inverted, kind='avg')
out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))

plt.imshow(out)
plt.show()