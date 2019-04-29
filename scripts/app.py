"""
Developed by Brihi Joshi
"""
import kivy
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.filechooser import FileChooserListView 
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
from io import BytesIO
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, segmentation
from skimage.color import convert_colorspace, rgba2rgb, hsv2rgb, rgb2gray, label2rgb
from skimage.future import graph
from PIL import Image as PImage
from functools import wraps
from array import array
import mido
import random

TEMP_PATH = "../assets/"


FLOAT_LAYOUT = FloatLayout(size=(300, 300))

title_label = Label(text="Rate of transfer (delay) in secs: 5",
				  font_size=20,
				  pos_hint={'x': .4, 'y': .8},
				  size_hint=(.2, .2))

speed_slider = Slider(min=0,
		 max=10, 
		 value=0.1,
		 step = 1,
		 pos_hint={'x': 0.5, 'y': 0.5},
		 size_hint=(.5, .8)
		 )

speed_slider_label = Label(text='Time Delay (in seconds) : ', font_size=15, pos_hint={'x': 0.47, 'y': 0.55}, size_hint=(.5, .8))
speed_slider_value_label = Label(text='0.0', font_size=15, pos_hint={'x': 0.70, 'y': 0.55}, size_hint=(.3, .8), bold=True)


# speed_slider = Slider(min=0, max=1, value=0.5, pos_hint={'x': 0.5, 'y': 0.4}, padding=2)
send_button = Button(text='Send', font_size=14, pos_hint={'x': 0.87, 'y': 0.05},size_hint=(0.12, 0.07))
# stop_button = Button(text='Stop', font_size=14, pos_hint={'x': 0.74, 'y': 0.05},size_hint=(0.12, 0.07))
send_status_label = Label(text='Press Send', font_size=15, pos_hint={'x': 0.87, 'y': 0.01}, size_hint=(0.12, 0.04), bold=True)

file_selector = Button(text = 'Select Image', pos_hint={'x': 0.01, 'y': 0.50},size_hint=(0.12, 0.07))

# Buttons for the colour preference image-

cp_coloured_button = CheckBox()
cp_coloured_button.text = 'Coloured'
cp_coloured_button.pos_hint = {'x': 0.07, 'y': 0.05}
cp_coloured_button.size_hint = (0.12, 0.07)
cp_coloured_button.group = 'colour_pref'
cp_coloured_button.active = True
cp_coloured_button.color = [128, 128, 128, 1]
cp_grayscale_button = CheckBox()
cp_grayscale_button.text = 'Gray Scale'
cp_grayscale_button.pos_hint = {'x': 0.27, 'y': 0.05}
cp_grayscale_button.size_hint = (0.12, 0.07)
cp_grayscale_button.group = 'colour_pref'
cp_grayscale_button.active = False
cp_grayscale_button.color = [128, 128, 128, 1]
cp_inverted_button = CheckBox()
cp_inverted_button.text = 'Inverted'
cp_inverted_button.pos_hint = {'x': 0.47, 'y': 0.05}
cp_inverted_button.size_hint = (0.12, 0.07)
cp_inverted_button.group = 'colour_pref'
cp_inverted_button.active = False
cp_inverted_button.color = [128, 128, 128, 1]


"""Colour Conversions"""

# hue_slider = Slider(min=0,
# 		 max=128, 
# 		 value=0,
# 		 step = 1,
# 		 pos_hint={'x': 0.2, 'y': 0.1},
# 		 size_hint=(.5, .5)
# 		 )




outport = mido.open_output('ILIAD - ImgTools', virtual=True, autoreset=True)
run_dict = {'v':5}
# global image_file


def send_RGB(r, g, b):
	print('ENTERED!!!!')

	# Just sending the MIDO messages
	outport.send(mido.Message('control_change', channel=1-1, control=16, value=r))
	outport.send(mido.Message('control_change', channel=1-1, control=17, value=g))
	outport.send(mido.Message('control_change', channel=1-1, control=18, value=b))


def yield_to_sleep(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		gen = func()
		def next_step(*_):
			try:
				t = next(gen)  # this executes 'func' before next yield and returns control to you
			except StopIteration:
				pass
			else:
				Clock.schedule_once(next_step, t)  # having control you can resume func execution after some time
		next_step()
	return wrapper


@yield_to_sleep  # use this decorator to cast 'yield' to non-blocking sleep
def read_image():
	print('ENTERED READ IMAGE')
	# img = mpimg.imread(image_chosen_path)
	# print('IMAGE READ')
	print(image_file)
	for i in range(len(image_file)):
		for j in range(len(image_file[0])):
			yield run_dict["v"]  # use yield to "sleep"
			r = int(image_file[i,j,0])
			g = int(image_file[i,j,1])
			b = int(image_file[i,j,2])
			print(r,g,b)
			send_RGB(r,g,b)
	send_status_label.text = 'Finished!'
	send_status_label.color = [0,128,0,1]



def OnSpeedSliderValueChange(instance,value):
	run_dict["v"] = value
	speed_slider_value_label.text = str(value)
	print(value, run_dict['v'])


def OnSendButtonPressed(instance):
	send_status_label.text = 'Sending...'
	send_status_label.color = [128,0,0,1]
	# print('ABOVE')
	# print(image_chosen_path)
	print('Send Button Pressed')
	# print(type(image_file))
	read_image()

# def OnHueSliderValueChange(instance, value):
# 	# print('ENTERED')
# 	# image_shape = image_file.shape
# 	# image_file_rgb = ""
# 	# if image_shape[2] == 4:
# 	# 	image_file_rgb = rgba2rgb(image_file)
# 	# elif image_shape[2] == 3:
# 	# 	image_file_rgb = image_file


# 	# image_file_hsv = convert_colorspace(image_file_rgb, 'RGB', 'HSV')

# 	# print(image_file_hsv[:,:,0])

# 	# image_file_hsv[:,:,0] = image_file_hsv[:,:,0] + value

# 	# print(image_file_hsv[:,:,0])

# 	# np.clip(image_file_hsv,0,1,out=image_file_hsv)

# 	# converted_rgb = hsv2rgb(image_file_hsv)

# 	# io.imsave(TEMP_PATH+'temp.jpg',converted_rgb)

# 	# disp_img.source = TEMP_PATH+'temp.jpg'

# 	# print(disp_img.source)

# 	# print(image_file_hsv.shape)

# 	# print('Conversion done')

# 	# disp_img.color = [value, disp_img.color[1], disp_img.color[2],disp_img.color[3]]

def OnCPColouredButtonPressed(instance, value):
	print('Pressed colour')

def OnCPGrayscaleButtonPressed(instance, value):
	print('Pressed Grayscale')
	print('ENTERED')
	image_shape = image_file.shape
	print(image_file.shape)

	image_file_gray = rgb2gray(np.flip(image_file,axis=0)).ravel()

	print(image_file_gray)

	# # buf1 = cv2.flip(image, 0)
	# buf = image_file_gray.tostring()
	# arr = array('B', image_file_gray)
	image_texture = Texture.create(size=(image_file.shape[1], image_file.shape[0]),colorfmt='luminance')
	image_texture.blit_buffer(np.float32(image_file_gray), colorfmt='luminance', bufferfmt='float')
	disp_img.texture = image_texture



	# image_file_gray_PIL = PImage.fromarray(image_file_gray.astype('uint8'))


	# data = BytesIO()
	# image_file_gray_PIL.save(data, format='png')
	# data.seek(0) # yes you actually need this
	# im = CoreImage(BytesIO(data.read()), ext='png')
	# disp_img.texture = im.texture

def OnCPInvertedButtonPressed(instance, value):
	print('Pressed Inverted')


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
	image_file_inverted = image_file

	labels = segmentation.slic(image_file_inverted, compactness=30, n_segments=400)
	g = graph.rag_mean_color(image_file_inverted, labels)

	labels2 = graph.merge_hierarchical(labels, g, thresh=35, rag_copy=False,
	                                   in_place_merge=True,
	                                   merge_func=merge_mean_color,
	                                   weight_func=_weight_mean_color)

	out = label2rgb(labels2, image_file_inverted, kind='avg')
	out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))

	# image_file_inverted = np.float32(image_file_inverted)

	image_texture = Texture.create(size=(image_file_inverted.shape[1], image_file_inverted.shape[0]),colorfmt='rgb')
	image_texture.blit_buffer(np.flip(np.float32(out),axis=0).ravel(), colorfmt='rgb', bufferfmt='float')
	disp_img.texture = image_texture

	print("DONE Inverted")



# def OnStopButtonPressed(instance):
# 	outport.reset()
# 	send_status_label.text = 'Stopped'
# 	send_status_label.color = [255,0,0,1]


class app(App):
	def create_popup(self, instance):
		# create popup layout
		content = BoxLayout(orientation='vertical', spacing=5)
		# popup_width = min(0.95 * Window.width, dp(500))
		self.filechooserpopup = Popup(
			title='Select video file', content=content, size_hint=(0.9, 0.9),
			width=(0.9,0.9))
	
		# create the filechooser
		self.filechooserview = FileChooserListView(
			# path=self.value,
			 size_hint=(1, 1), filters=['*.png','*.jpg'])
	
		# construct the content
		content.add_widget(self.filechooserview)
		# content.add_widget(SettingSpacer())
	
		# 2 buttons are created for accept or cancel the current value
		btnlayout = BoxLayout(size_hint_y=None, height='40dp', spacing='40dp')
		btn = Button(text='Ok')

		btn.bind(on_release=self.select_image_file_path)
		btnlayout.add_widget(btn)
		btn = Button(text='Cancel')
		btn.bind(on_release=self.filechooserpopup.dismiss)
		btnlayout.add_widget(btn)
		content.add_widget(btnlayout)
	
		# all done, open the popup !
		self.filechooserpopup.open()

	def select_image_file_path(self, instance):
		global image_chosen_path, image_file
		# videofilepath = self.filechooserview.selection
		print(self.filechooserview.selection)
		if len(self.filechooserview.selection) == 0:
			content = BoxLayout(orientation='vertical', spacing=5)
			popup = Popup(
			title='Please select a file!', content=content, size_hint=(0.2, 0.2),
			width=(0.2,0.2))
			btn = Button(text='Ok')
			btn.bind(on_release=popup.dismiss)
			content.add_widget(btn)
			popup.open()
		else:
			image_chosen_path = self.filechooserview.selection[0]
			image_file = io.imread(image_chosen_path)
			print(image_chosen_path,'HELLLOOOO')
			# videofilepath = self.filechooserview.selection[0]
			self.filechooserpopup.dismiss()
			# FLOAT_LAYOUT.remove_widget(disp_img)
			disp_img.source = image_chosen_path

			speed_slider.disabled = False
			send_button.disabled = False
			# hue_slider.disabled = False


	def build(self):

		global disp_img

		disp_img = Image(source='../assets/init_back.jpg',pos_hint={'x': 0.01, 'y': 0.58},keep_ratio=True, size_hint=(0.45,0.45))
		FLOAT_LAYOUT.add_widget(disp_img)
		FLOAT_LAYOUT.add_widget(file_selector)

		FLOAT_LAYOUT.add_widget(speed_slider)
		FLOAT_LAYOUT.add_widget(speed_slider_label)
		FLOAT_LAYOUT.add_widget(speed_slider_value_label)


		FLOAT_LAYOUT.add_widget(send_button)
		# FLOAT_LAYOUT.add_widget(stop_button)
		FLOAT_LAYOUT.add_widget(send_status_label)

		# FLOAT_LAYOUT.add_widget(hue_slider)

		FLOAT_LAYOUT.add_widget(cp_coloured_button)
		FLOAT_LAYOUT.add_widget(cp_grayscale_button)
		FLOAT_LAYOUT.add_widget(cp_inverted_button)


		speed_slider.bind(value=OnSpeedSliderValueChange)
		send_button.bind(on_press=OnSendButtonPressed)
		# stop_button.bind(on_press=OnStopButtonPressed)
		file_selector.bind(on_press = self.create_popup)

		# hue_slider.bind(value=OnHueSliderValueChange)

		speed_slider.disabled = True
		send_button.disabled = True
		# hue_slider.disabled = True

		# Colour Preferences buttons

		cp_coloured_button.bind(active=OnCPColouredButtonPressed)
		cp_grayscale_button.bind(active=OnCPGrayscaleButtonPressed)
		cp_inverted_button.bind(active=OnCPInvertedButtonPressed)

		
		return FLOAT_LAYOUT

	# def calculate(self, *args):
	# 	print(args)


if __name__ == '__main__':

	app().run()
