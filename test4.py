from functools import wraps

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import  FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


FLOAT_LAYOUT = FloatLayout(size=(300, 300))

s = Slider(min=0, max=5, value=25)

run_dict = {'v':5}

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
def test_function():
    for i in range(10000):
        yield run_dict["v"]  # use yield to "sleep"
        print('Called', run_dict['v'])

def OnSliderValueChange(instance,value):
    run_dict["v"] = value
    print(value, run_dict['v'])


class TestApp(App):
    def build(self):
        test_function()
        FLOAT_LAYOUT.add_widget(s)
        
        s.bind(value=OnSliderValueChange)

        return FLOAT_LAYOUT



if __name__ == '__main__':
    TestApp().run()