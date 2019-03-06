import kivy
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import  FloatLayout
from kivy.config import Config
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

import mido
import cv2
import numpy as np
import time

Config.set('kivy', 'keyboard_mode', 'systemandmulti')

FLOAT_LAYOUT = FloatLayout(size=(300, 300))

title_label = Label(text="Rate of transfer (delay) in secs: 5",
				  font_size=20,
				  pos_hint={'x': .4, 'y': .8},
				  size_hint=(.2, .2))

text_box = TextInput(multiline=False,
					 font_size=20,
					 pos_hint={'x': .4, 'y': .3},
					 size_hint=(.2, .2)
					 )

# class MyButton(ButtonBehavior, Image):

# 	def __init__(self, **kwargs):
# 		super(MyButton, self).__init__(**kwargs)
# 		self.source = 'C:\\Users\\Aditya Adhikary\\Desktop\\ILIAD\\button_play.png'

# 	def on_release(self):
# 		OnRunButtonPressed()

	# def on_press(self):



def OnRunButtonPressed(instance):
	sleep_time=0.15
	rtmidi = mido.Backend('mido.backends.rtmidi')
	# portmidi = mido.Backend('mido.backends.portmidi')

	# inputport = rtmidi.open_input()
	# outputport = rtmidi.open_output('loopMIDI Port 1', virtual=True) #gives windows error
	# outputport = portmidi.open_output('loopMIDI Port 1', virtual=True) #gives windows error
	midiports = mido.get_output_names()
	print(midiports[1])
	outputport = rtmidi.open_output(midiports[1]) #try 

	print(cv2.__version__)
	vidcap = cv2.VideoCapture('test_video.mp4')
	success,image = vidcap.read()
	count = 0
	success = True

	while success:
		# cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
		success,image = vidcap.read()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# print('Read a new frame with shape: ', gray.shape)
		count += 1

		# for i in range(5):
		note = np.mean(gray)
		# print(note)
		# note = np.mean(note)
		# print(note)
		note=note//2
		print(note)
		# print(type(note))
		msg = mido.Message('note_on', note=int(note))
		outputport.send(msg)
		print('Sent message ', msg, " : " , count)
		time.sleep(sleep_time)

run_button = Button(text='Run',
					font_size=20,
					pos_hint={'x': .4, 'y': .1},
					size_hint=(.2, .1),
					# on_press=OnRunButtonPressed
					)


slider1 = Slider(min=0.01,
			 max=10, 
			 value=5,
			 pos_hint={'x': .1, 'y': .1},
			 size_hint=(.2, .1),
			 )

kivy.clock.Clock = None

def OnSliderValueChange(instance,value):
	title_label.text = "Rate of transfer (delay) in secs: " + str(value)

	#TODO: interrupt the timer of the sending of messages

class kivi_app(App):
	def build(self):
		FLOAT_LAYOUT.add_widget(title_label)
		# FLOAT_LAYOUT.add_widget(text_box)
		FLOAT_LAYOUT.add_widget(run_button)
		FLOAT_LAYOUT.add_widget(slider1)
		slider1.bind(value=OnSliderValueChange)
		run_button.bind(on_press=OnRunButtonPressed)
		return FLOAT_LAYOUT

	def calculate(self, *args):
		print(args)


if __name__ == '__main__':

	kivi_app().run()

	# TODO: need to put the following stuff on a different thread