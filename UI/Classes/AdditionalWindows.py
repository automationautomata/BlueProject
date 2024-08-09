import kivy
kivy.require('1.9.0')

from kivy.uix.popup import Popup

global app


class SortingWindow(Popup):
    def __init__(self, **kwargs):
        super(SortingWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()
