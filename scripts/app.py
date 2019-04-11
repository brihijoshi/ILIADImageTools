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
from functools import wraps
import mido
import random


FLOAT_LAYOUT = FloatLayout(size=(300, 300))

title_label = Label(text="Rate of transfer (delay) in secs: 5",
				  font_size=20,
				  pos_hint={'x': .4, 'y': .8},
				  size_hint=(.2, .2))

send_slider = Slider(min=0, max=5, value=25, pos_hint={'x': 0.5, 'y': 0.4})
send_button = Button(text='Send', font_size=14, pos_hint={'x': 0.85, 'y': 0.15},size_hint=(0.15, 0.15))

file_selector = Button(text = 'Select Image', pos_hint={'x': 0.01, 'y': 0.2},size_hint=(0.15, 0.15))


outport = mido.open_output('New', virtual=True, autoreset=True)
run_dict = {'v':5}


def send_RGB(r):

	# Just sending the MIDO messages
	outport.send(mido.Message('control_change', channel=1-1, control=16, value=r))
	# outport.send(mido.Message('control_change', channel=1+1, control=17, value=g))
	# outport.send(mido.Message('control_change', channel=1+1, control=17, value=b))


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
	for i in range(10000):
		yield run_dict["v"]  # use yield to "sleep"
		r = random.randint(10, 90)
		# g = random.randint(, 40)
		# b = random.randint(30, 50)
		send_RGB(r)


def OnSliderValueChange(instance,value):
	run_dict["v"] = value
	print(value, run_dict['v'])

def OnButtonPressed(instance):
	print('Button Pressed!!!!!')


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
			self.image_chosen_path = self.filechooserview.selection
			# videofilepath = self.filechooserview.selection[0]
			self.filechooserpopup.dismiss()
			disp_img = Image(source=self.image_chosen_path[0],pos_hint={'x': 0.01, 'y': 0.5},keep_ratio=True, size_hint=(0.5,0.5))
			FLOAT_LAYOUT.add_widget(disp_img)
			# stopped = 2
			# self.file_path_text.text = '...' + videofilepath[-50:]


	def build(self):
		
		FLOAT_LAYOUT.add_widget(file_selector)
		FLOAT_LAYOUT.add_widget(send_slider)
		FLOAT_LAYOUT.add_widget(send_button)

		send_slider.bind(value=OnSliderValueChange)
		send_button.bind(on_press=OnButtonPressed)
		file_selector.bind(on_press = self.create_popup)
		
		return FLOAT_LAYOUT

	# def calculate(self, *args):
	# 	print(args)


if __name__ == '__main__':

	app().run()
