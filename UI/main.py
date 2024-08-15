import kivy
import Classes.Buttons
import Classes.Table
import Classes.Screens
import Classes.AdditionalWindows
kivy.require('1.9.0')

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder


Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', 'false')
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '600')
Config.write()
Builder.load_file('MyMain.kv')

class TestApp(App):
    def __init__(self, **kwargs):
        App.__init__(self)
        self.current_theme = 0
        self.themes = [
                {
                    'Base': [[0, .01, .2], [.1, .1, .5], [.2, .2, .5]],
                    'Additionally': [[.01, .3, .3], [.05, .4, .3], [.2, .35, .3], [.007, .25, .25]],
                    'Accent': [[.9, .05, .3], [.9, .3, .5], [.65, .05, .2]],
                    'Text': [1, 1, 1]
                },
                {
                    'Base': [[.85, .9, 1], [.75, .8, .9], [.75, .75, .9]],
                    'Additionally': [[.85, .6, .8], [.75, .5, .7], [.85, .7, .85], [.8, .55, .75]],
                    'Accent': [[.9, .8, .05], [.8, .7, .01], [.9, .8, .3]],
                    'Text': [0, 0, 0]
                },
                {
                    'Base': [[.15, .1, 0], [.15, .15, .05], [.3, .15, 0]],
                    'Additionally': [[.35, .25, .05], [.4, .3, .15], [.5, .4, .3], [.3, .2, .01]],
                    'Accent': [[.05, .04, .03], [.25, .25, .25], [.97, .96, .95]],
                    'Text': [1, 1, 1]
                },
                {
                    'Base': [[.8, .8, .8], [.95, .95, .95], [.65, .65, .65]],
                    'Additionally': [[.1, .45, .1], [.15, .4, .15], [.35, .55, .35], [.05, .4, .05]],
                    'Accent': [[0, 0, .6], [.1, .1, .7], [.25, .25, .8]],
                    'Text': [0, 0, 0]
                }]
        global app
        app = self

    def build(self):
        Classes.Buttons.app = app
        Classes.Table.app = app
        Classes.Screens.app = app
        Classes.AdditionalWindows.app = app
        ms = Classes.Screens.MainScreen()

        return ms

if __name__ == '__main__':
    TestApp().run()