"""
Developed by Brihi Joshi
"""
import kivy
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import  FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import wraps
import mido
import random


FLOAT_LAYOUT = FloatLayout(size=(300, 300))

title_label = Label(text="Rate of transfer (delay) in secs: 5",
				  font_size=20,
				  pos_hint={'x': .4, 'y': .8},
				  size_hint=(.2, .2))

s = Slider(min=0, max=5, value=25)

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


class app(App):

	def build(self):
		FLOAT_LAYOUT.add_widget(s)
		s.bind(value=OnSliderValueChange)
		read_image()

		return FLOAT_LAYOUT

	def calculate(self, *args):
		print(args)


if __name__ == '__main__':

	app().run()
