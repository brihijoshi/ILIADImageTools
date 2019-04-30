# -*- coding: utf-8 -*-
"""
Developed by Brihi Joshi
"""
from kivy.config import Config
Config.set('graphics', 'resizable', False)
# Config.set('kivy','default_font',['../assets/NotoSans-Light.ttf'])
# Config.set('graphics', 'width', '600')
# Config.set('graphics', 'height', '800')

import kivy
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
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
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from skimage.transform import swirl, PiecewiseAffineTransform, warp
from skimage import util
from skimage.measure import block_reduce
import numpy as np
from skimage import io, segmentation
from skimage.color import convert_colorspace, rgba2rgb, hsv2rgb, rgb2gray, label2rgb, rgb2hsv, gray2rgb
from skimage.future import graph
from functools import wraps
from array import array
import mido
import random
import os

# Widget.font_name: '../assets/NotoSans-Light.ttf'

# if 'KIVY_DOC' not in os.environ:
#     _default_font_paths = literal_eval(Config.get('kivy', 'default_font'))
#     DEFAULT_FONT = _default_font_paths.pop(0)
# else:
#     DEFAULT_FONT = None

# Label.register(DEFAULT_FONT, ['../assets/NotoSans-Light.ttf'])

FONT = '../assets/NotoSans-Light.ttf'



class ILIADImgTools(App):  # display the welcome screen
	def build(self):
		sm = ScreenManager()
		sm.add_widget(WelcomeScreen(name='welcomeScreen'))
		sm.add_widget(FunctionScreen(name='functionScreen'))
		return sm

class WelcomeScreen(Screen): #welcomeScreen subclass
	def __init__(self, **kwargs): #constructor method
		super(WelcomeScreen, self).__init__(**kwargs) #init parent
		welcomePage = FloatLayout()
		iliad_logo = Image(source='../assets/img_tools_logo.png',pos_hint={'top': 0.9, 'center_x': 0.5},keep_ratio=True, size_hint=(0.9, 0.7))

		continue_button = Button(font_name=FONT,text= 'Continue', on_press=self.callback,pos_hint={'y': 0.1, 'x': 0.40} , size_hint=(0.15, 0.08))
		
		# welcomeBox = Button(font_name=FONT,text= 'Click to continue', on_press=self.callback,pos_hint={'bottom': 0.5, 'center_x': 0.5} )

		welcomePage.add_widget(iliad_logo)
		welcomePage.add_widget(continue_button)

		self.add_widget(welcomePage)

	def callback(self, instance):
		print('The button has been pressed')
		self.manager.current = 'functionScreen'

class FunctionScreen(Screen):  #For later function navigation
	def __init__(self, **kwargs): #constructor method
		super(FunctionScreen, self).__init__(**kwargs) #init parent
		# FLOAT_LAYOUT = FloatLayout()
		# functionLabel = Label(font_name=FONT,text='Welcome to the function page. Here you will choose what functions to use',
		#                       halign='center', valign='center', size_hint=(0.4,0.2), pos_hint={'top': 1, 'center_x': 0.5})
		# print('ENTERED')
		# FLOAT_LAYOUT.add_widget(functionLabel)
		
		# self.add_widget(FLOAT_LAYOUT)

		FLOAT_LAYOUT = FloatLayout(size=(300, 300))

		outport = mido.open_output('ILIAD - ImgTools', virtual=True, autoreset=True)
		run_dict = {'v':0}
		image_file_dict = {'image_file':"", 'orig_image':""}
		channel_dict = {'channel':1}
		tv_props = {'func':None, 'block_length':0, 'block_width':0, 'type':'lin_horizontal', 'block_depth':0}
		tv_wid_list = []
		should_stop = {'flag':False}

		logo = Image(source='../assets/img_tools_logo.png',pos_hint={'x': 0.19, 'y': 0.48},keep_ratio=True, size_hint=(0.20, 0.12))

		with logo.canvas:
			Line(points=[385, 600, 385, 85], width=0.25)
			Line(points=[385, 370, 800, 370], width=0.25)
			Line(points=[385, 85, 800, 85], width=0.25)
			Line(points=[0, 85, 385, 85], width=0.25)

		TEMP_PATH = "../assets/"


		

		speed_slider = Slider(min=0,
				 max=10, 
				 value=0.1,
				 step = 1,
				 pos_hint={'x': 0.5, 'y': 0.5},
				 size_hint=(.5, .8)
				 )

		speed_slider_label = Label(font_name=FONT,text='Time Delay (in seconds) : ', font_size=17, pos_hint={'x': 0.47, 'y': 0.55}, size_hint=(.5, .8))
		speed_slider_value_label = Label(font_name=FONT,text='0.0', font_size=17, pos_hint={'x': 0.72, 'y': 0.55}, size_hint=(.3, .8), bold=True)


		# speed_slider = Slider(min=0, max=1, value=0.5, pos_hint={'x': 0.5, 'y': 0.4}, padding=2)
		send_button = Button(font_name=FONT,text='Send', font_size=14, pos_hint={'x': 0.87, 'y': 0.05},size_hint=(0.12, 0.07))
		# stop_button = Button(font_name=FONT,text='Stop', font_size=14, pos_hint={'x': 0.74, 'y': 0.05},size_hint=(0.12, 0.07))
		send_status_label = Label(font_name=FONT,text='Press Send', font_size=17, pos_hint={'x': 0.87, 'y': 0.01}, size_hint=(0.12, 0.04), bold=True)

		file_selector = Button(font_name=FONT,text = 'Select Image', pos_hint={'x': 0.01, 'y': 0.50},size_hint=(0.12, 0.07))

		reset_button = Button(font_name=FONT,text='Reset', font_size=14, pos_hint={'x': 0.72, 'y': 0.05},size_hint=(0.12, 0.07))

		stop_button = Button(font_name=FONT,text='Stop', font_size=14, pos_hint={'x': 0.57, 'y': 0.05},size_hint=(0.12, 0.07))

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

		colour_filter_label = Label(font_name=FONT,text='Colour Filters', font_size=17, pos_hint={'x': 0.12, 'y': 0.26}, size_hint=(.05, .17))
		invert_filter_label = Label(font_name=FONT,text='Invert', font_size=14, pos_hint={'x': 0.02, 'y': 0.15}, size_hint=(.05, .17))
		grayscale_filter_label = Label(font_name=FONT,text='Grayscale', font_size=14, pos_hint={'x': 0.12, 'y': 0.15}, size_hint=(.05, .17))
		animate_filter_label = Label(font_name=FONT,text='Animate', font_size=14, pos_hint={'x': 0.22, 'y': 0.15}, size_hint=(.05, .17))


		transformation_label = Label(font_name=FONT,text='Transform', font_size=17, pos_hint={'x': 0.37, 'y': 0.26}, size_hint=(.05, .17))
		transform_dropdown = Spinner(font_name=FONT,
			# default value shown
			text='Select Transform',
			# available values
			values=('Swirl','Wave'),
			# just for positioning in our example
			pos_hint={'x': 0.32, 'y': 0.21}, size_hint=(.15, .10))

		cc_chanel_label = Label(font_name=FONT,text='CC Channel Used', font_size=17, pos_hint={'x': 0.85, 'y': 0.72}, size_hint=(.05, .17))
		cc_chanel_value = Label(font_name=FONT,text='None', font_size=17, pos_hint={'x': 0.85, 'y': 0.65}, size_hint=(.05, .17))




		def OnTransformDropdownSelect(spinner, text):
			if text=='Swirl':

				image_to_swirl = image_file_dict['image_file']

				if len(image_to_swirl.shape) ==2:

					image_to_swirl = gray2rgb(image_to_swirl)

				swirled = swirl(image_to_swirl, rotation=0, strength=10, radius=400)

				image_file_dict['image_file'] = swirled

				
				image_texture = Texture.create(size=(swirled.shape[1], swirled.shape[0]),colorfmt='rgb')
				image_texture.blit_buffer(np.float32(np.flip(swirled,axis=0).ravel()), colorfmt='rgb', bufferfmt='float')
				disp_img.texture = image_texture


			if text == 'Wave':

				image = image_file_dict['image_file']

				if len(image.shape) == 2:

					image = gray2rgb(image)

				rows, cols = image.shape[0], image.shape[1]

				src_cols = np.linspace(0, cols, 20)
				src_rows = np.linspace(0, rows, 10)
				src_rows, src_cols = np.meshgrid(src_rows, src_cols)
				src = np.dstack([src_cols.flat, src_rows.flat])[0]

				# add sinusoidal oscillation to row coordinates
				dst_rows = src[:, 1] - np.sin(np.linspace(0, 3 * np.pi, src.shape[0])) * 50
				dst_cols = src[:, 0]
				dst_rows *= 1.5
				dst_rows -= 1.5 * 50
				dst = np.vstack([dst_cols, dst_rows]).T


				tform = PiecewiseAffineTransform()
				tform.estimate(src, dst)

				out_rows = image.shape[0] - 1.5 * 50
				out_cols = cols
				out = warp(image, tform, output_shape=(out_rows, out_cols))

				image_file_dict['image_file'] = out

				image_texture = Texture.create(size=(out.shape[1], out.shape[0]),colorfmt='rgb')
				image_texture.blit_buffer(np.float32(np.flip(out,axis=0).ravel()), colorfmt='rgb', bufferfmt='float')
				disp_img.texture = image_texture



		channel_values = []
		for i in range(1,17):
			channel_values.append("Channel "+str(i))

		channel_dropdown = Spinner(font_name=FONT,
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

		channel_dropdown = Spinner(font_name=FONT,
			# default value shown
			text='Select Channel',
			# available values
			values=tuple(channel_values),
			# just for positioning in our example
			pos_hint={'x': 0.50, 'y': 0.65}, size_hint=(.2, .1))

		channel_label = Label(font_name=FONT,text='Channel', font_size=17, pos_hint={'x': 0.50, 'y': 0.75}, size_hint=(.2, .1))



		hue_slider = Slider(min=0,
				 max=1, 
				 value= 0,
				 step = 0.01,
				 pos_hint={'x': 0.02, 'y': 0.40},
				 size_hint=(.23, .01)
				 )

		hue_slider_label = Label(font_name=FONT,text='Hue', font_size=17, pos_hint={'x': 0.02, 'y': 0.45}, size_hint=(.23, .01))

		saturation_slider = Slider(min=0,
				 max=1, 
				 value= 0,
				 step = 0.01,
				 pos_hint={'x': 0.25, 'y': 0.40},
				 size_hint=(.23, .01)
				 )

		saturation_slider_label = Label(font_name=FONT,text='Saturation', font_size=17, pos_hint={'x': 0.25, 'y': 0.45}, size_hint=(.23, .01))



		image_traversal_label = Label(font_name=FONT,text='Image Traversal', font_size=22, pos_hint={'x': 0.70, 'y': 0.48}, size_hint=(.05, .17), bold = True)


		tv_linear_button = CheckBox()
		tv_linear_button.pos_hint = {'x': 0.60, 'y': 0.40}
		tv_linear_button.size_hint = (0.05, 0.17)
		tv_linear_button.group = 'tv_pref'
		tv_linear_button.active = False
		tv_linear_button.color = [128, 128, 128, 1]
		tv_block_button = CheckBox()
		tv_block_button.pos_hint = {'x': 0.80, 'y': 0.40}
		tv_block_button.size_hint = (0.05, 0.17)
		tv_block_button.group = 'tv_pref'
		tv_block_button.active = False
		tv_block_button.color = [128, 128, 128, 1]
		# tv_skip_button = CheckBox()
		# tv_skip_button.pos_hint = {'x': 0.85, 'y': 0.40}
		# tv_skip_button.size_hint = (0.05, 0.17)
		# tv_skip_button.group = 'tv_pref'
		# tv_skip_button.active = False
		# tv_skip_button.color = [128, 128, 128, 1]

		tv_linear_label = Label(font_name=FONT,text='Linear', font_size=14, pos_hint={'x': 0.60, 'y': 0.35}, size_hint=(.05, .17))
		tv_block_label = Label(font_name=FONT,text='Block', font_size=14, pos_hint={'x': 0.80, 'y': 0.35}, size_hint=(.05, .17))
		# tv_skip_label = Label(font_name=FONT,text='Skip', font_size=14, pos_hint={'x': 0.85, 'y': 0.35}, size_hint=(.05, .17))

		# tv_fix = Button(font_name=FONT,text='Fix Traversal', font_size=14, pos_hint={'x':0.87, 'y': 0.18},size_hint=(0.12, 0.07))

		mwl_label = Label(font_name=FONT,text=u'Made with <3 \nby Brihi', font_size=14, pos_hint={'x': 0.05, 'y': 0.02}, size_hint=(.05, .07))



		def send_MIDI(r, g=None, b=None):
			print('ENTERED!!!!')

			channel = channel_dict['channel']

			if g is not None and b is not None:

				# Just sending the MIDO messages
				outport.send(mido.Message('control_change', channel=channel-1, control=16, value=r))
				outport.send(mido.Message('control_change', channel=channel-1, control=17, value=g))
				outport.send(mido.Message('control_change', channel=channel-1, control=18, value=b))

			elif g is not None:

				outport.send(mido.Message('control_change', channel=channel-1, control=16, value=r))
				outport.send(mido.Message('control_change', channel=channel-1, control=17, value=g))


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
			print(temp)
			if len(temp.shape) == 3:
				if type(temp[0,0,0]) == np.float64:
					temp = temp * 255
			elif len(temp.shape) == 2:
				if type(temp[0,0]) == np.float64:
					temp = temp * 255

			if tv_props['type'] == 'lin_horizontal':

				if len(temp[0,0]) == 3:
					cc_chanel_value.text = '\nCC Number 16\nCC Number 17\nCC Number 18'
				elif len(temp[0,0]) == 2:
					cc_chanel_value.text = '\nCC Number 16\nCC Number 17'
				elif len(temp[0,0]) == 1:
					cc_chanel_value.text = '\nCC Number 16'

			elif tv_props['type'] == 'lin_vertical' or tv_props['type'] == 'block':
				cc_chanel_value.text = '\nCC Number 16'
			# Will check for traversal type here

			if tv_props['type'] == 'lin_horizontal':

				for i in range(len(temp)):
					for j in range(len(temp[0])):
						yield run_dict["v"]  # use yield to "sleep"
						if (should_stop['flag']==True):
							stop_button.disabled = True
							print('ENDED', should_stop['flag'])
							break
						if len(temp.shape) == 3:
							if len(temp[i,j])==3:
								r = np.clip(int(temp[i,j,0]),0,127)
								g = np.clip(int(temp[i,j,1]),0,127)
								b = np.clip(int(temp[i,j,2]),0,127)
								print(r,g,b)
								send_MIDI(r,g,b)
							elif len(temp[i,j]) == 2:
								r = np.clip(int(temp[i,j,0]),0,127)
								g = np.clip(int(temp[i,j,1]),0,127)
								send_MIDI(r,g)
							else:
								for k in range(len(temp[i,j])):
									r =  np.clip(int(temp[i,j,k]),0,127)
									send_MIDI(r)

						elif len(temp.shape) == 2:
							print(temp[i,j])
							send_MIDI(np.clip(int(temp[i,j]),0,127))

			elif tv_props['type'] == 'lin_vertical':
				for i in range(len(temp)):
					for j in range(len(temp[0,0])):
						yield run_dict["v"]  # use yield to "sleep"
						if (should_stop['flag']==True):
							# should_stop['flag']==False
							stop_button.disabled = True
							break
						for k in range(len(temp[0])):
							r =  np.clip(int(temp[i,k,j]),0,127)
							print(r)
							send_MIDI(r)

			elif tv_props['type'] == 'block':
				print('TRYING TO SEND BLOCK DATA')
				block_arr = block_reduce(image=temp,\
					block_size=(tv_props['block_depth'],tv_props['block_length'],tv_props['block_width']),\
					func = tv_props['func'])
				print(len(block_arr))
				print(len(block_arr[0]))
				print(len(block_arr[0][0]))
				for i in range(len(block_arr)):
					for j in range(len(block_arr[0])):
						yield run_dict["v"]  # use yield to "sleep"
						if (should_stop['flag']==True):
							# should_stop['flag']==False
							stop_button.disabled = True
							break
						for k in range(len(block_arr[0][0])):
							r =  np.clip(int(block_arr[i,j,k]),0,127)
							send_MIDI(r)



			if should_stop['flag'] == True:
				send_status_label.text = 'Stopped!'
				send_status_label.color = [128,0,0,1]
			else:
				send_status_label.text = 'Finished!'
				send_status_label.color = [0,128,0,1]

			cc_chanel_value.text = 'None'
			should_stop['flag']=False
			stop_button.disabled = True
			








		def OnSpeedSliderValueChange(instance,value):
			run_dict["v"] = value
			speed_slider_value_label.text = str(value)
			print(value, run_dict['v'])


		def OnSendButtonPressed(instance):
			stop_button.disabled = False
			send_status_label.text = 'Sending...'
			send_status_label.color = [128,0,0,1]
			# print('ABOVE')
			# print(image_chosen_path)
			print('Send Button Pressed')
			# print(type(image_file))
			read_image()

		def OnStopButtonPressed(instance):
			should_stop['flag'] = True
			send_status_label.text = 'Stopping...'
			send_status_label.color = [128,0,0,1]


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
			print(value, instance)
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

			image_file_dict['image_file'] = gray2rgb(rgb2gray(image_file))

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

		def OnTVLinearText(spinner, text):
			if text == 'Horizontal':
				tv_props['func'] = None
				tv_props['block_length'] = 0
				tv_props['block_width'] = 0
				tv_props['type'] = 'lin_horizontal'
			elif text == 'Vertical':
				tv_props['func'] = None
				tv_props['block_length'] = 0
				tv_props['block_width'] = 0
				tv_props['type'] = 'lin_vertical'


		def OnTVLinearButtonPressed(instance, value):
			if len(tv_wid_list)!=0:
				#Empty Widget List
				for wid in tv_wid_list:
					FLOAT_LAYOUT.remove_widget(wid)
				del tv_wid_list[:]

			lin_tv_label = Label(font_name=FONT,text='Linear Traversal Type', font_size=17, pos_hint={'x': 0.68, 'y': 0.30}, size_hint=(0.12, 0.07))

			tv_linear_dropdown = Spinner(font_name=FONT,
				# default value shown
				text='Select Traversal',
				# available values
				values=('Horizontal', 'Vertical'),
				# just for positioning in our example
				pos_hint={'x': 0.66, 'y': 0.23}, size_hint=(0.15, 0.07))

			tv_wid_list.append(lin_tv_label)
			tv_wid_list.append(tv_linear_dropdown)

			FLOAT_LAYOUT.add_widget(lin_tv_label)
			FLOAT_LAYOUT.add_widget(tv_linear_dropdown)
			tv_linear_dropdown.bind(text=OnTVLinearText)

		def OnTVBlockDepthText(spinner, text):
			tv_props['block_depth'] = int(text)

		def OnTVBlockLengthText(spinner, text):
			tv_props['block_length'] = int(text)

		def OnTVBlockWidthText(spinner, text):
			tv_props['block_width'] = int(text)

		def OnTVBlockFuncText(spinner, text):
			if text == 'Maximum':
				tv_props['func'] = np.max
			elif text == 'Minimum':
				tv_props['func'] = np.min
			elif text == 'Average':
				tv_props['func'] = np.mean
			elif text == 'Median':
				tv_props['func'] = np.median
			elif text == 'Sum':
				tv_props['func'] = np.sum

		 

		def OnTVBlockButtonPressed(instance, value):
			if len(tv_wid_list)!=0:
				#Empty Widget List
				for wid in tv_wid_list:
					FLOAT_LAYOUT.remove_widget(wid)
				del tv_wid_list[:]

			depth_values = []
			for i in range(len(image_file_dict['image_file'])):
				depth_values.append(str(i+1))

			depth_input_label = Label(font_name=FONT,text='Depth Size', font_size=17, pos_hint={'x': 0.55, 'y': 0.37}, size_hint=(0.10, 0.03))

			depth_input_dropdown = Spinner(font_name=FONT,
				# default value shown
				text='Select Depth',
				# available values
				values=depth_values,
				# just for positioning in our example
				pos_hint={'x': 0.52, 'y': 0.29}, size_hint=(0.15, 0.07))

			length_values = []  
			for i in range(len(image_file_dict['image_file'][0])):
				length_values.append(str(i+1))

			length_input_label = Label(font_name=FONT,text='Length Size', font_size=17, pos_hint={'x': 0.71, 'y': 0.37}, size_hint=(0.10, 0.03))

			length_input_dropdown = Spinner(font_name=FONT,
				# default value shown
				text='Select Length',
				# available values
				values=length_values,
				# just for positioning in our example
				pos_hint={'x': 0.68, 'y': 0.29}, size_hint=(0.15, 0.07))

			width_values = []   
			for i in range(len(image_file_dict['image_file'][0][0])):
				width_values.append(str(i+1))

			width_input_label = Label(font_name=FONT,text='Width Size', font_size=17, pos_hint={'x': 0.85, 'y': 0.37}, size_hint=(0.10, 0.03))

			width_input_dropdown = Spinner(font_name=FONT,
				# default value shown
				text='Select Width',
				# available values
				values=width_values,
				# just for positioning in our example
				pos_hint={'x': 0.84, 'y': 0.29}, size_hint=(0.15, 0.07))

			func_input_label = Label(font_name=FONT,text='Aggregation Function', font_size=17, pos_hint={'x': 0.70, 'y': 0.25}, size_hint=(0.10, 0.03))

			func_input_dropdown = Spinner(font_name=FONT,
				# default value shown
				text='Select Function',
				# available values
				values=('Maximum','Minimum','Average','Median','Sum'),
				# just for positioning in our example
				pos_hint={'x': 0.67, 'y': 0.17}, size_hint=(0.15, 0.07))


			tv_wid_list.append(depth_input_label)
			tv_wid_list.append(depth_input_dropdown)
			tv_wid_list.append(length_input_label)
			tv_wid_list.append(length_input_dropdown)
			tv_wid_list.append(width_input_label)
			tv_wid_list.append(width_input_dropdown)
			tv_wid_list.append(func_input_label)
			tv_wid_list.append(func_input_dropdown)

			FLOAT_LAYOUT.add_widget(depth_input_label)
			FLOAT_LAYOUT.add_widget(depth_input_dropdown)
			FLOAT_LAYOUT.add_widget(length_input_label)
			FLOAT_LAYOUT.add_widget(length_input_dropdown)
			FLOAT_LAYOUT.add_widget(width_input_label)
			FLOAT_LAYOUT.add_widget(width_input_dropdown)
			FLOAT_LAYOUT.add_widget(func_input_label)
			FLOAT_LAYOUT.add_widget(func_input_dropdown)

			depth_input_dropdown.bind(text=OnTVBlockDepthText)
			length_input_dropdown.bind(text=OnTVBlockLengthText)
			width_input_dropdown.bind(text=OnTVBlockWidthText)
			func_input_dropdown.bind(text=OnTVBlockFuncText)

			tv_props['type'] = 'block'

		def create_popup(instance):

			global filechooserpopup, filechooserview
			# create popup layout
			content = BoxLayout(orientation='vertical', spacing=5)
			# popup_width = min(0.95 * Window.width, dp(500))
			filechooserpopup = Popup(
				title='Select video file', content=content, size_hint=(0.9, 0.9),
				width=(0.9,0.9))
		
			# create the filechooser
			filechooserview = FileChooserListView(
				# path=self.value,
				 size_hint=(1, 1), filters=['*.png','*.jpg'])
		
			# construct the content
			content.add_widget(filechooserview)
			# content.add_widget(SettingSpacer())
		
			# 2 buttons are created for accept or cancel the current value
			btnlayout = BoxLayout(size_hint_y=None, height='40dp', spacing='40dp')
			btn = Button(font_name=FONT,text='Ok')

			btn.bind(on_release=select_image_file_path)
			btnlayout.add_widget(btn)
			btn = Button(font_name=FONT,text='Cancel')
			btn.bind(on_release=filechooserpopup.dismiss)
			btnlayout.add_widget(btn)
			content.add_widget(btnlayout)
		
			# all done, open the popup !
			filechooserpopup.open()

		def select_image_file_path(instance):
			global image_chosen_path, image_file, orig_image_texture
			# videofilepath = self.filechooserview.selection
			print(filechooserview.selection)
			if len(filechooserview.selection) == 0:
				content = BoxLayout(orientation='vertical', spacing=5)
				popup = Popup(
				title='Please select a file!', content=content, size_hint=(0.2, 0.2),
				width=(0.2,0.2))
				btn = Button(font_name=FONT,text='Ok')
				btn.bind(on_release=popup.dismiss)
				content.add_widget(btn)
				popup.open()
			else:
				image_chosen_path = filechooserview.selection[0]
				image_file = io.imread(image_chosen_path)
				image_file_dict['image_file']=image_file
				image_file_dict['orig_image'] = image_file
				print(image_chosen_path,'HELLLOOOO')
				# videofilepath = self.filechooserview.selection[0]
				filechooserpopup.dismiss()
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
				tv_linear_button.disabled = False
				tv_block_button.disabled = False
				# tv_skip_button.disabled = False
				# tv_fix.disabled = False

		disp_img = Image(source='../assets/init_back.jpg',pos_hint={'x': 0.01, 'y': 0.58},keep_ratio=True, size_hint=(0.45,0.45))
		FLOAT_LAYOUT.add_widget(disp_img)
		FLOAT_LAYOUT.add_widget(logo)
		FLOAT_LAYOUT.add_widget(file_selector)

		FLOAT_LAYOUT.add_widget(speed_slider)
		FLOAT_LAYOUT.add_widget(speed_slider_label)
		FLOAT_LAYOUT.add_widget(speed_slider_value_label)


		FLOAT_LAYOUT.add_widget(send_button)
		FLOAT_LAYOUT.add_widget(stop_button)
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

		FLOAT_LAYOUT.add_widget(image_traversal_label)
		FLOAT_LAYOUT.add_widget(tv_linear_button)
		FLOAT_LAYOUT.add_widget(tv_block_button)
		# FLOAT_LAYOUT.add_widget(tv_skip_button)

		FLOAT_LAYOUT.add_widget(tv_linear_label)
		FLOAT_LAYOUT.add_widget(tv_block_label)
		FLOAT_LAYOUT.add_widget(cc_chanel_label)
		FLOAT_LAYOUT.add_widget(cc_chanel_value)
		FLOAT_LAYOUT.add_widget(mwl_label)
		# FLOAT_LAYOUT.add_widget(tv_skip_label)
		# FLOAT_LAYOUT.add_widget(tv_fix)


		speed_slider.bind(value=OnSpeedSliderValueChange)
		send_button.bind(on_press=OnSendButtonPressed)
		stop_button.bind(on_press=OnStopButtonPressed)
		# stop_button.bind(on_press=OnStopButtonPressed)
		file_selector.bind(on_press = create_popup)
		reset_button.bind(on_press = OnResetButtonPressed)
		channel_dropdown.bind(text=OnChannelDropdownSelect)

		transform_dropdown.bind(text=OnTransformDropdownSelect)

		# hue_slider.bind(value=OnHueSliderValueChange)

		speed_slider.disabled = True
		send_button.disabled = True
		stop_button.disabled = True
		reset_button.disabled = True
		hue_slider.disabled = True
		saturation_slider.disabled = True
		cp_inverted_button.disabled = True
		cp_grayscale_button.disabled = True
		cp_animated_button.disabled = True
		transform_dropdown.disabled = True
		tv_linear_button.disabled = True
		tv_block_button.disabled = True
		# tv_skip_button.disabled = True
		# tv_fix.disabled = True

		# Colour Preferences buttons

		cp_inverted_button.bind(active=OnCPInvertedButtonPressed)
		cp_grayscale_button.bind(active=OnCPGrayscaleButtonPressed)
		cp_animated_button.bind(active=OnCPanimatedButtonPressed)

		hue_slider.bind(value=OnHueSliderChange)
		saturation_slider.bind(value=OnSaturationSliderChange)

		tv_linear_button.bind(active=OnTVLinearButtonPressed)
		tv_block_button.bind(active=OnTVBlockButtonPressed)


		self.add_widget(FLOAT_LAYOUT)


if __name__ == '__main__':
	ILIADImgTools().run()