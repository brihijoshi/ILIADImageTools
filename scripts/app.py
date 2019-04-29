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
from kivy.uix.spinner import Spinner
from kivy.graphics import *
from skimage.transform import swirl
from skimage import util
from io import BytesIO
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, segmentation
from skimage.color import convert_colorspace, rgba2rgb, hsv2rgb, rgb2gray, label2rgb, rgb2hsv, gray2rgb
from skimage.future import graph
from PIL import Image as PImage
from functools import wraps
from array import array
import mido
import random
import copy


outport = mido.open_output('ILIAD - ImgTools', virtual=True, autoreset=True)
run_dict = {'v':0}
image_file_dict = {'image_file':"", 'orig_image':""}
channel_dict = {'channel':1}
cc_dict = {'cc':16}


TEMP_PATH = "../assets/"


FLOAT_LAYOUT = FloatLayout(size=(300, 300))

speed_slider = Slider(min=0,
		 max=10, 
		 value=0.1,
		 step = 1,
		 pos_hint={'x': 0.5, 'y': 0.5},
		 size_hint=(.5, .8)
		 )

speed_slider_label = Label(text='Time Delay (in seconds) : ', font_size=17, pos_hint={'x': 0.47, 'y': 0.55}, size_hint=(.5, .8))
speed_slider_value_label = Label(text='0.0', font_size=17, pos_hint={'x': 0.70, 'y': 0.55}, size_hint=(.3, .8), bold=True)


# speed_slider = Slider(min=0, max=1, value=0.5, pos_hint={'x': 0.5, 'y': 0.4}, padding=2)
send_button = Button(text='Send', font_size=14, pos_hint={'x': 0.87, 'y': 0.05},size_hint=(0.12, 0.07))
# stop_button = Button(text='Stop', font_size=14, pos_hint={'x': 0.74, 'y': 0.05},size_hint=(0.12, 0.07))
send_status_label = Label(text='Press Send', font_size=17, pos_hint={'x': 0.87, 'y': 0.01}, size_hint=(0.12, 0.04), bold=True)

file_selector = Button(text = 'Select Image', pos_hint={'x': 0.01, 'y': 0.50},size_hint=(0.12, 0.07))

reset_button = Button(text='Reset', font_size=14, pos_hint={'x': 0.87, 'y': 0.15},size_hint=(0.12, 0.07))

# Buttons for the colour preference image-

cp_inverted_button = CheckBox()
cp_inverted_button.pos_hint = {'x': 0.02, 'y': 0.20}
cp_inverted_button.size_hint = (0.05, 0.17)
cp_inverted_button.group = 'colour_pref'
cp_inverted_button.active = False
cp_inverted_button.color = [128, 128, 128, 1]
cp_grayscale_button = CheckBox()
cp_grayscale_button.pos_hint = {'x': 0.12, 'y': 0.20}
cp_grayscale_button.size_hint = (0.05, 0.17)
cp_grayscale_button.group = 'colour_pref'
cp_grayscale_button.active = False
cp_grayscale_button.color = [128, 128, 128, 1]
cp_animated_button = CheckBox()
cp_animated_button.pos_hint = {'x': 0.22, 'y': 0.20}
cp_animated_button.size_hint = (0.05, 0.17)
cp_animated_button.group = 'colour_pref'
cp_animated_button.active = False
cp_animated_button.color = [128, 128, 128, 1]

colour_filter_label = Label(text='Colour Filters', font_size=17, pos_hint={'x': 0.12, 'y': 0.26}, size_hint=(.05, .17))
invert_filter_label = Label(text='Invert', font_size=14, pos_hint={'x': 0.02, 'y': 0.15}, size_hint=(.05, .17))
grayscale_filter_label = Label(text='Grayscale', font_size=14, pos_hint={'x': 0.12, 'y': 0.15}, size_hint=(.05, .17))
animate_filter_label = Label(text='Animate', font_size=14, pos_hint={'x': 0.22, 'y': 0.15}, size_hint=(.05, .17))


transformation_label = Label(text='Transform', font_size=17, pos_hint={'x': 0.37, 'y': 0.26}, size_hint=(.05, .17))
transform_dropdown = Spinner(
	# default value shown
	text='Select Transform',
	# available values
	values=('Swirl','Nothing'),
	# just for positioning in our example
	pos_hint={'x': 0.32, 'y': 0.21}, size_hint=(.15, .10))

def OnTransformDropdownSelect(spinner, text):
	if text=='Swirl':

		image_to_swirl = image_file_dict['image_file']

		swirled = swirl(image_to_swirl, rotation=0, strength=10, radius=400)

		image_file_dict['image_file'] = swirled

		
		image_texture = Texture.create(size=(swirled.shape[1], swirled.shape[0]),colorfmt='rgb')
		image_texture.blit_buffer(np.float32(np.flip(swirled,axis=0).ravel()), colorfmt='rgb', bufferfmt='float')
		disp_img.texture = image_texture



channel_values = []
for i in range(1,17):
	channel_values.append("Channel "+str(i))

channel_dropdown = Spinner(
	# default value shown
	text='Select Channel',
	# available values
	values=tuple(channel_values),
	# just for positioning in our example
	pos_hint={'x': 0.50, 'y': 0.75}, size_hint=(.2, .1))

def OnChannelDropdownSelect(spinner, text):
	channel_dict['channel'] = int(text.split(" ")[-1])
	print(channel_dict['channel'])

channel_values = []
for i in range(1,17):
	channel_values.append("Channel "+str(i))

channel_dropdown = Spinner(
	# default value shown
	text='Select Channel',
	# available values
	values=tuple(channel_values),
	# just for positioning in our example
	pos_hint={'x': 0.50, 'y': 0.65}, size_hint=(.2, .1))

channel_label = Label(text='Channel', font_size=17, pos_hint={'x': 0.50, 'y': 0.75}, size_hint=(.2, .1))



hue_slider = Slider(min=0,
		 max=1, 
		 value= 0,
		 step = 0.01,
		 pos_hint={'x': 0.02, 'y': 0.40},
		 size_hint=(.23, .01)
		 )

hue_slider_label = Label(text='Hue', font_size=17, pos_hint={'x': 0.02, 'y': 0.45}, size_hint=(.23, .01))

saturation_slider = Slider(min=0,
		 max=1, 
		 value= 0,
		 step = 0.01,
		 pos_hint={'x': 0.25, 'y': 0.40},
		 size_hint=(.23, .01)
		 )

saturation_slider_label = Label(text='Saturation', font_size=17, pos_hint={'x': 0.25, 'y': 0.45}, size_hint=(.23, .01))






def send_MIDI(r, g=None, b=None):
	print('ENTERED!!!!')

	channel = channel_dict['channel']

	if g is not None and b is not None:

		# Just sending the MIDO messages
		outport.send(mido.Message('control_change', channel=channel-1, control=16, value=r))
		outport.send(mido.Message('control_change', channel=channel-1, control=17, value=g))
		outport.send(mido.Message('control_change', channel=channel-1, control=18, value=b))

	else:

		outport.send(mido.Message('control_change', channel=channel-1, control=16, value=r))



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
	temp = image_file_dict['image_file']
	print((temp == image_file_dict['orig_image']))
	if len(temp.shape) == 3:
		if (temp == image_file_dict['orig_image']).all() == False:
			temp = temp * 255
	elif len(temp.shape) == 2:
		if temp != image_file_dict['orig_image']:
			temp = temp * 255

	
	print(temp)
	for i in range(len(temp)):
		for j in range(len(temp[0])):
			yield run_dict["v"]  # use yield to "sleep"
			if len(temp.shape) == 3:
				r = np.clip(int(temp[i,j,0]),0,127)
				g = np.clip(int(temp[i,j,1]),0,127)
				b = np.clip(int(temp[i,j,2]),0,127)
				print(r,g,b)
				send_MIDI(r,g,b)
			elif len(temp.shape) == 2:
				print(temp[i,j])
				send_MIDI(np.clip(int(temp[i,j]),0,127))

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

def OnResetButtonPressed(instance):

	disp_img.texture = orig_image_texture
	cp_inverted_button.active = False
	cp_grayscale_button.active = False
	cp_animated_button.active = False
	transform_dropdown.text = 'Select Transform'
	hue_slider.value = 0
	saturation_slider.value = 0
	image_file_dict['image_file'] = io.imread(image_chosen_path)


def OnCPInvertedButtonPressed(instance, value):
	print('Pressed inverted')
	print('ENTERED')
	image_shape = image_file.shape
	print(image_file.shape)

	image_file_inverted = util.invert(np.flip(image_file,axis=0)).ravel()/255


	image_file_dict['image_file'] = util.invert(image_file)/255

	# # buf1 = cv2.flip(image, 0)
	# buf = image_file_gray.tostring()
	# arr = array('B', image_file_gray)
	image_texture = Texture.create(size=(image_file.shape[1], image_file.shape[0]),colorfmt='rgb')
	image_texture.blit_buffer(np.float32(image_file_inverted), colorfmt='rgb', bufferfmt='float')
	disp_img.texture = image_texture

def OnCPGrayscaleButtonPressed(instance, value):
	print('Pressed Grayscale')
	print('ENTERED')
	image_shape = image_file.shape
	print(image_file.shape)

	image_file_gray = rgb2gray(np.flip(image_file,axis=0)).ravel()

	print('GRASCALE HERE --------')

	image_file_dict['image_file'] = rgb2gray(image_file)

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

def OnCPanimatedButtonPressed(instance, value):
	print('Pressed animated')


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
	image_file_animated = image_file

	labels = segmentation.slic(image_file_animated, compactness=30, n_segments=400)
	g = graph.rag_mean_color(image_file_animated, labels)

	labels2 = graph.merge_hierarchical(labels, g, thresh=35, rag_copy=False,
									   in_place_merge=True,
									   merge_func=merge_mean_color,
									   weight_func=_weight_mean_color)

	out = label2rgb(labels2, image_file_animated, kind='avg')
	out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))

	image_file_dict['image_file'] = out

	print(out)

	# image_file_animated = np.float32(image_file_animated)

	image_texture = Texture.create(size=(image_file_animated.shape[1], image_file_animated.shape[0]),colorfmt='rgb')
	image_texture.blit_buffer(np.flip(np.float32(out),axis=0).ravel(), colorfmt='rgb', bufferfmt='float')
	disp_img.texture = image_texture

	print("DONE animated")

def TintImageHue(hue):
	""" Add color of the given hue to an RGB image.

	By default, set the saturation to 1 so that the colors pop!
	"""
	temp = image_file_dict['image_file']

	print('--------------- HUE ---------------')
	print(temp)

	if len(temp.shape) == 3:


		hsv = rgb2hsv(temp)
		hsv[:, :, 0] = hue

		print(hsv2rgb(hsv))

		print('--------------- HUE ---------------')
		return hsv2rgb(hsv)

	elif len(temp.shape) == 2:

		rgb = gray2rgb(temp)
		hsv = rgb2hsv(rgb)
		hsv[:, :, 0] = hue

		print(hsv2rgb(hsv))

		print('--------------- HUE ---------------')
		return hsv2rgb(hsv)


def OnHueSliderChange(instance,value):
	temp = TintImageHue(value)
	image_file_dict['image_file'] = temp
	print(image_file_dict['image_file'])

	image_texture = Texture.create(size=(temp.shape[1], temp.shape[0]),colorfmt='rgb')
	image_texture.blit_buffer(np.flip(np.float32(temp),axis=0).ravel(), colorfmt='rgb', bufferfmt='float')
	disp_img.texture = image_texture

def TintImageSaturation(saturation):
	""" Add color of the given hue to an RGB image.

	By default, set the saturation to 1 so that the colors pop!
	"""
	temp = image_file_dict['image_file']

	print(temp)

	if len(temp.shape) == 3:

		hsv = rgb2hsv(temp)
		hsv[:, :, 1] = saturation

		print(hsv2rgb(hsv))
		return hsv2rgb(hsv)
	elif len(temp.shape) == 2:

		rgb = gray2rgb(temp)
		hsv = rgb2hsv(rgb)
		hsv[:, :, 1] = saturation

		print(hsv2rgb(hsv))
		return hsv2rgb(hsv)


def OnSaturationSliderChange(instance,value):
	temp = TintImageSaturation(value)
	image_file_dict['image_file'] = temp
	print(image_file_dict['image_file'])

	image_texture = Texture.create(size=(temp.shape[1], temp.shape[0]),colorfmt='rgb')
	image_texture.blit_buffer(np.flip(np.float32(temp),axis=0).ravel(), colorfmt='rgb', bufferfmt='float')
	disp_img.texture = image_texture




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
		global image_chosen_path, image_file, orig_image_texture
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
			image_file_dict['image_file']=image_file
			image_file_dict['orig_image'] = image_file
			print(image_chosen_path,'HELLLOOOO')
			# videofilepath = self.filechooserview.selection[0]
			self.filechooserpopup.dismiss()
			# FLOAT_LAYOUT.remove_widget(disp_img)
			disp_img.source = image_chosen_path
			orig_image_texture = disp_img.texture

			speed_slider.disabled = False
			send_button.disabled = False
			reset_button.disabled = False
			hue_slider.disabled = False
			saturation_slider.disabled = False
			cp_inverted_button.disabled = False
			cp_grayscale_button.disabled = False
			cp_animated_button.disabled = False
			transform_dropdown.disabled = False


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
		FLOAT_LAYOUT.add_widget(reset_button)

		# FLOAT_LAYOUT.add_widget(hue_slider)

		FLOAT_LAYOUT.add_widget(cp_inverted_button)
		FLOAT_LAYOUT.add_widget(cp_grayscale_button)
		FLOAT_LAYOUT.add_widget(cp_animated_button)
		FLOAT_LAYOUT.add_widget(channel_dropdown)

		FLOAT_LAYOUT.add_widget(hue_slider)
		FLOAT_LAYOUT.add_widget(hue_slider_label)

		FLOAT_LAYOUT.add_widget(saturation_slider)
		FLOAT_LAYOUT.add_widget(saturation_slider_label)

		FLOAT_LAYOUT.add_widget(colour_filter_label)
		FLOAT_LAYOUT.add_widget(invert_filter_label)
		FLOAT_LAYOUT.add_widget(grayscale_filter_label)
		FLOAT_LAYOUT.add_widget(animate_filter_label)

		FLOAT_LAYOUT.add_widget(channel_label)
		FLOAT_LAYOUT.add_widget(transformation_label)
		FLOAT_LAYOUT.add_widget(transform_dropdown)


		speed_slider.bind(value=OnSpeedSliderValueChange)
		send_button.bind(on_press=OnSendButtonPressed)
		# stop_button.bind(on_press=OnStopButtonPressed)
		file_selector.bind(on_press = self.create_popup)
		reset_button.bind(on_press = OnResetButtonPressed)
		channel_dropdown.bind(text=OnChannelDropdownSelect)

		transform_dropdown.bind(text=OnTransformDropdownSelect)

		# hue_slider.bind(value=OnHueSliderValueChange)

		speed_slider.disabled = True
		send_button.disabled = True
		reset_button.disabled = True
		hue_slider.disabled = True
		saturation_slider.disabled = True
		cp_inverted_button.disabled = True
		cp_grayscale_button.disabled = True
		cp_animated_button.disabled = True
		transform_dropdown.disabled = True

		# Colour Preferences buttons

		cp_inverted_button.bind(active=OnCPInvertedButtonPressed)
		cp_grayscale_button.bind(active=OnCPGrayscaleButtonPressed)
		cp_animated_button.bind(active=OnCPanimatedButtonPressed)

		hue_slider.bind(value=OnHueSliderChange)
		saturation_slider.bind(value=OnSaturationSliderChange)

		
		return FLOAT_LAYOUT

	# def calculate(self, *args):
	# 	print(args)


if __name__ == '__main__':

	app().run()
