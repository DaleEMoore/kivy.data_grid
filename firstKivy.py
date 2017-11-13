#!/usr/bin/env python2
# From http://missmaximas-programmer.blogspot.com/2015/05/python-with-ui-kivy-basics.html
import kivy
from kivy.app import App
from kivy.uix.button import Button

__version__ = "1.0"


class FirstApp(App):
    def build(self):
        return Button(text='Hello World')

if __name__ == '__main__':
    FirstApp().run()
